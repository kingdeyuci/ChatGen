
# Habana Setup

Workloads that require to use the Intel Habana Gaudi AI Accelerator must specify a `HAS-SETUP-HABANA-GAUDI` label.

## System Setup

- [Instructions for installing the Habana Container Runtime][Installation guide]

## Node Labels

The following node label is available on the worker node:

- `HAS-SETUP-HABANA-GAUDI=yes`: Optional

## See Also

- [Kuberentes User Guide][Kuberentes User Guide]


[Installation guide]: https://docs.habana.ai/en/latest/Installation_Guide/shared/Set_up_Container_Usage_Bare_Metal.html?highlight=container%20runtime#install-container-runtime
[Kuberentes User Guide]: https://docs.habana.ai/en/latest/Orchestration/Gaudi_Kubernetes/index.html
