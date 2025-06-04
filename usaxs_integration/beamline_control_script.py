import os
import uuid
import time
import datetime
import subprocess
import shlex
import pathlib

import pandas as pd
import numpy as np

from AFL.automation.APIServer.Client import Client
from tiled.client import from_uri
from tiled.queries import Eq, Contains

###############
### CONFIG ####
###############
date_format =  "%Y-%m-%d %H:%M:%S"

local_working_directory = pathlib.Path('/home/beams/USAXS/Apps/AFL/Pozzo/')
local_data_path = local_working_directory / 'data' # where the local data files will be written

data_package_filename = "packet.txt"

remote_host = "18.216.44.137"
remote_username = "ubuntu"
remote_filepath = pathlib.Path("~/usaxs_queue/") 
remote_datapath = pathlib.Path("~/usaxs_data/")
pem_path = # path to pem key goes here 

loop_wait_time = 10 #seconds to wait in between pinging remote file

capillary_x = 198.2
capillary_y = 35.5
###################
### END CONFIG ####
###################

def copy_remote_file(instance_ip, user_name, remote_path, local_path, pem_path,copy_from=True):
    """
    Copies a remote file to the local machine using scp.

    Args:
        instance_ip (str): The public IP address or public DNS of the EC2 instance.
        user_name (str): The username for connecting to the EC2 instance (e.g., 'ec2-user' or 'ubuntu').
        remote_path (str): The full path to the file on the EC2 instance.
        local_path (str): The full path where the file should be saved locally.
        pem_path (str): The path to the .pem file used for SSH authentication.
    """
    # print(instance_ip)
    # print(user_name)
    # print(remote_path)
    # print(local_path)
    # print(pem_path)
    try:
        command = [
            "scp",
            "-i",
            str(pem_path),
        ]
        if copy_from:
            command.extend([
                f"{user_name}@{instance_ip}:{remote_path}",
                str(local_path),
            ])
        else:
            command.extend([
                str(local_path),
                f"{user_name}@{instance_ip}:{remote_path}",
            ])
        
        subprocess.run(shlex.split(' '.join(command)), check=True, capture_output=True)
        print(f"File copied successfully from {remote_path} to {local_path}")
    
    except subprocess.CalledProcessError as e:
         print(f"Error copying file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Connect to and configure AFL USAXS Server
usaxs = Client('usaxscontrol',5000)
usaxs.login('nb')
usaxs.set_config(
    platemap = {
        '6A':{ 
            'SlotA': { 
                'x0': capillary_x, 
                'y0': capillary_y, 
                'x_step': 9, 
                'y_step': 9, 
                'x_per_y_skew': 0.0,
                'y_per_x_skew': 0.0, 
            }
        }
    }
)
usaxs.enqueue(task_name='setPosition',plate='SlotA',row='A',col=1,x_offset=0,y_offset=0) #should only need to do this once

# Connect to AFL Tiled Database
c = from_uri( 
    'http://usaxscontrol:8007', 
    api_key='key goes here' 
)


last_datetime = None
while True:
    print(f'Attempting to download {data_package_filename} from {remote_host}...')
    copy_remote_file(
        remote_host,
        remote_username,
        remote_filepath / data_package_filename,
        local_working_directory / data_package_filename,
        pem_path,
        copy_from=True
    )

    print(f'Reading file and attempting to parse contents...')
    with open(data_package_filename,'r') as f:
        data = [line for line in f]

    if len(data)==0:
        print(f'Data file {data_package_filename} was empty, waiting for new file...' )
        time.sleep(loop_wait_time)
        continue
        
    new_datetime = datetime.datetime.strptime(data[0].strip(), date_format)
    if (last_datetime is None) or (new_datetime==last_datetime):
        if last_datetime is None:
            last_datetime = new_datetime
            print(f'No "last_datetime" set. Storing last_datetime = {last_datetime}' )
        else:
            print(f'New datetime is identical to old, waiting for new file...' )
        time.sleep(loop_wait_time)
        continue
    else:
        #store new_datetime as "last datetime"
        last_datetime = new_datetime

    date_str = data[0].strip()
    sample_name = data[1].strip()
    sample_composition = data[2].strip()
    sample_uid = data[3].strip()
    print(f'Found file with new datetime: {date_str}' )
    print(f'Preparing to measure sample "{sample_name}"' )
    print(f'Sample composition: {sample_composition}' )
    print(f'Assigned sample uuid: {sample_uid}' )

    print(f'Triggering USAXS...' )
    usaxs.enqueue(
        task_name='set_sample', 
        sample_name=sample_name, 
        sample_uuid=sample_uid,
        sample_composition=sample_composition
    )
    queue_uid = usaxs.enqueue(task_name='expose', name=sample_name, reduce_USAXS=True, reduce_WAXS=True)
    usaxs.wait(target_uuid=queue_uid)

    print(f'Looking for data in tiled...' )
    tiled_result = c.search(Eq('sample_uuid',sample_uid))
    if len(tiled_result)==0:
        raise ValueError(f'Cound not find tiled entry for measurement sample_uid={sample_uid}')

    print(f'Writing USAXS data locally...' )
    usaxs_q   = tiled_result.search(Eq('array_name','USAXS_q')).items()[-1][-1][()]
    usaxs_int = tiled_result.search(Eq('array_name','USAXS_int')).items()[-1][-1][()]
    usaxs_sub = tiled_result.search(Eq('array_name','USAXS_sub')).items()[-1][-1][()]
    usaxs_data = np.vstack([usaxs_q,usaxs_int,usaxs_sub]).T
    usaxs_filename = f'USAXS-{sample_name}-{sample_uid}.csv'
    np.savetxt(fname=local_data_path/usaxs_filename,X=usaxs_data,delimiter=',',header='#q, USAXS_int, USAXS_sub')
        
    print(f'Writing WAXS data locally...' )
    waxs_q   = tiled_result.search(Eq('array_name','WAXS_q')).items()[-1][-1][()]
    waxs_int = tiled_result.search(Eq('array_name','WAXS_int')).items()[-1][-1][()]
    waxs_data = np.vstack([waxs_q,waxs_int]).T
    waxs_filename = f'WAXS-{sample_name}-{sample_uid}.csv'
    np.savetxt(fname=local_data_path/waxs_filename,X=waxs_data,delimiter=',',header='#q, WAXS_int')

    print(f'Writing USAXS data to remote host...' )
    copy_remote_file(
        remote_host,
        remote_username,
        remote_datapath / usaxs_filename,
        local_data_path / usaxs_filename,
        pem_path,
        copy_from=False,
    )
    
    print(f'Writing WAXS data to remote host...' )
    copy_remote_file(
        remote_host,
        remote_username,
        remote_datapath / waxs_filename,
        local_data_path / waxs_filename,
        pem_path,
        copy_from=False,
    )
    
    time.sleep(loop_wait_time)