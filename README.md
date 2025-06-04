# Automated Mesoporous Synthesis

This repository is a companion to the paper, "Open-hardware automation platform for accelerated sol-gel nanomaterial synthesis". It contains the execution code used to run the automated synthesis experiments as well as a tutorial walk-through detailing how to reproduce the synthesis workflow.

## Repository structure:

- APS experiments:
  |- automated execution: Fully automated experiments using the NIST-AFL sample loader. 
    |- Jubilee/AFL execution notebook
    |- sample composition table
    |- usaxs_integration.md - writeup of the details of USAXS integration we used.

  |- batch experiments: Batch synthesized experiments, measured using liquid cartridge plates in batch mode due to timing constraints.
    |- Execution notebook
    |- Constrained sobol rejection sampling notebook
    |- Compositions of synthesized samples
    |- 

- Tutorial walkthrough: 
  | walkthrough.md - guide to re-producing the workflow described here
  | automated_synthesis.ipynb - example notebook showing how to synthesize particles and use AFL sample changer. Cleaned up version of actual experiment execution code. 