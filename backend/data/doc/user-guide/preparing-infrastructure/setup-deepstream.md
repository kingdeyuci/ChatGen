# Deepstream SDK Setup

Workloads that require to use the NVIDIA DeepStream SDK must specify a `HAS-SETUP-NVIDIA-CUDA` label.

## System Setup

- [Instructions for NVIDIA's dGPU Setup for Ubuntu][setup instructions]

## Node Labels

The following node label is available on the worker node:

- `HAS-SETUP-NVIDIA-CUDA=yes`: Optional

## See Also

- [Nvidia DeepStream Documentation][Nvidia DeepStream Documentation]


[setup instructions]: https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_Quickstart.html#dgpu-setup-for-ubuntu
[Nvidia DeepStream Documentation]: https://docs.nvidia.com/metropolis/deepstream/dev-guide/text/DS_Overview.html