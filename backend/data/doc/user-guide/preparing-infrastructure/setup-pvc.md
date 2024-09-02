# Setup PVC

Ponte Vecchio (PVC) is Intel Xe HPC Exascale GPU for high performance computing. Workloads that require to use the Intel® Data Center GPU Max Series must specify a `HAS-SETUP-PVC` label.

## System Setup

- [Instructions for the PVC driver setup][setup instructions]

## Node Labels

The following node label is available on the worker node:

- `HAS-SETUP-PVC=yes`: Optional


[setup instructions]: https://dgpu-docs.intel.com/driver/installation.html