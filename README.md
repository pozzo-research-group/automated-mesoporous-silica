# Automated Mesoporous Synthesis

This repository is a companion to the paper, "Open-hardware automation platform for accelerated sol-gel nanomaterial synthesis". It contains the execution code used to run the automated synthesis experiments as well as a tutorial walk-through detailing how to reproduce the synthesis workflow.

<img src="Tutorial/jubilee_usaxs.png">

## Repository contents

synthesis_experiment_files/
├── fully_automated_execution/                     # Files for the fully automated execution of synthesis - characterization experiments
│   ├── 2025_03_28_BaselineSampling.ipynb          # Fully automated experiments using NIST-AFL sample loader
|   ├── Sobol_baseline_sample_generation.ipynb     # Constrained Sobol rejection sampling to select sample compositions
│   ├── Mesoporous_SobolBaseline_APS_RestrictedAmmoniaTEOS_3_28_25.csv         # Sample compositions used for these experiments. 
│   ├── 2025_03_28_BaselineSampling.log            # Log file generated from experiment
│   ├── Mesoporous_constants_APS.json              # Constants for parameter space
│   └── systemconfig.json                          # AFL and system config
├── batch_synthesis/                               # Files for batch-mode experiment synthesis, results in paper are from these experiments.
│   ├── 2025_03_29_BatchSynthesis.ipynb                # Notebook for executing batch-synthesized experiments
│   ├── Sobol_baseline_sample_generation_batchmode.ipynb     # Constrained Sobol rejection sampling for batch mode experiments
│   ├── Mesoporous_SobolBaseline_APS_BatchMode_3_29_25.csv   # Compositions of selected samples
│   ├── Mesoporous_constants_APS_batch.json        # Constants for batch mode parameter space
│   ├── APS_batchSynthesis_2025_03_29.log          # Log file from batch synthesis experiment
│   └── systemconfig.json                          # AFL and system config
Tutorial/                                          # Instructional walkthrough of how to reproduce synthesis shown here
├── tutorial.md                                    # Step-by-step guide to reproducing the workflow
└── TutorialWalkthrough.ipynb                      # Tutorial walk-through notebook
usaxs_integration/                                 # Details on the automated USAXS instrument integration
├── usaxs_integration.md                           # Details of USAXS integration used
└──  beamline_control_script.py                    # Component of beamline integration
sample_utilities/                                  # Utilities for sample selection and synthesis volume calculations
└── samples.py
stober_synthesis_utils.py                          # Utilities for reactant transfer and sample mixing
usaxs_utils.py                                     # Utilities for USAXS instrument integration - client

  ## Procedure tutorial

  For an explanatory walk-through of the steps needed to set up and execute the synthesis described in the paper, check out the [tutorial](Tutorial/tutorial.md)

  ## Instrument integration

  More information on the APS 12-ID-E USAXS and Xenocs SAXS instrument integrations is available [here](usaxs_integration/usaxs_integration.md).

  ## Additional hardware documentation

  The science-jubilee platform, including the Digital Pipette syringe tools, is fully documented [here](https://science-jubilee.readthedocs.io/en/latest/)

  The NIST-AFL sample changer implementation is documented [here](https://github.com/pozzo-research-group/AFL-sample-loader/tree/main).