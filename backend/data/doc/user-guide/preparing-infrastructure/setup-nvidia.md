# Setup NVIDIA

Workloads that require to use the AWS NVIDIA CUDA Accelerator must specify a `HAS-SETUP-NVIDIA-CUDA` label.

## System Setup

- [Instructions for the Inferentia neuron runtime package setup][setup instructions]

## Node Labels

The following node label is available on the worker node:

- `HAS-SETUP-NVIDIA-CUDA=yes`: Optional

## See Also

- [Nvidia Cuda Setup and Install][Nvidia Cuda Setup and Install]


[setup instructions]: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#package-manager-metas
[Nvidia Cuda Setup and Install]: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#package-manager-metas