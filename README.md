# Automated Mesoporous Synthesis

This repository is a companion to the paper, "Open-hardware automation platform for accelerated sol-gel nanomaterial synthesis". It contains the execution code used to run the automated synthesis experiments as well as a tutorial walk-through detailing how to reproduce the synthesis workflow.

## Repository structure:


📁 APS-experiments/
├── 📁 automated-execution/
│   ├── 📓 Jubilee_AFL_execution.ipynb          # Fully automated experiments using NIST-AFL sample loader
│   ├── 📄 sample_composition_table.csv
│   └── 📄 usaxs_integration.md                 # Details of USAXS integration used
│
├── 📁 batch-experiments/
│   ├── 📓 batch_execution.ipynb                # Notebook for executing batch-synthesized experiments
│   ├── 📓 constrained_sobol_sampling.ipynb     # Constrained Sobol rejection sampling
│   └── 📄 synthesized_sample_compositions.csv
│
📁 tutorial-walkthrough/
├── 📄 walkthrough.md                           # Step-by-step guide to reproducing the workflow
└── 📓 automated_synthesis.ipynb                # Clean example notebook using AFL sample changer



  ## Procedure tutorial

  For an explanatory walk-through of the steps needed to set up and execute the synthesis described in the paper, check out the [tutorial](Tutorial/tutorial.md)

  ## Instrument integration

  More information on the APS 12-ID-E USAXS and Xenocs SAXS instrument integrations is available [here](usaxs_integration/usaxs_integration.md).

  ## Additional hardware documentation

  The science-jubilee platform, including the Digital Pipette syringe tools, is fully documented [here](https://science-jubilee.readthedocs.io/en/latest/)

  The NIST-AFL sample changer implementation is documented [here](https://github.com/pozzo-research-group/AFL-sample-loader/tree/main).