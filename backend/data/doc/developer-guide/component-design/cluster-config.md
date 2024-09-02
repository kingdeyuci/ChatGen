# Specifying the cluster configuration

The `cluster-config.yaml` manifest describes the machine specification to run the workloads. The specification is still evolving and subject to change.

The following example describes a 3-node cluster to be used in some workload:

```yaml
cluster:
  - labels: {}
  - labels: {}
  - labels: {}
```

The `cluster-config.yaml` consists of the following sections:

- **`cluster`**: This section defines the post-Sil cluster configurations.

## cluster.labels

The `cluster.labels` section describes any must have system level setup that a workload must use. The setup is specified in terms of a set of Kubernetes node labels as follows:

| Label | Description |
|:-----:|:------------|
| `HAS-SETUP-QAT` | This label specifies that the QAT kernel driver must be installed and configured on the system. Any workload that uses the QAT HW feature must specify this label. If the workload must work with a specific version or OS of the QAT HW, use the following labels instead: `HAS-SETUP-QAT-CENTOS8`, `HAS-SETUP-QAT-KERNEL-V0512`, `HAS-SETUP-QAT-V200`.<br>See also: [QAT In-Tree Setup][QAT In-Tree Setup] and [QAT Out-Of-Tree Setup][QAT Out-Of-Tree Setup]. |   
| `HAS-SETUP-DSA` | This label specifies that DSA must be configured on the system. Any workload that uses the DSA feature must specify this label.<br>See also: [DSA Setup][DSA Setup]. | 
| `HAS-SETUP-MEMORY` | This label specifies the minimum memory required by the workload. See also: [Memory Setup][Memory Setup]. | 
| `HAS-SETUP-IAA` | This label is not implemented yet. It suppose to specify that IAA must be configured on the system. Any workload that uses the IAA feature must specify this label.<br>See also: [IAA Setup][IAA Setup]. | 
| `HAS-SETUP-DLB` | This label specifies that DLB must be available on the system. Any workload that uses the DLB feature must specify this label.<br>See also: [DLB Setup][DLB Setup]. |
| `HAS-SETUP-NIC` | This set of labels specify that high-speed network interconnect is required. As every worker must have network connection (default `1Gbps`) to form a Kubernetes cluster, there is no `HAS-SETUP-NIC` label. Instead, if a workload requires higher bandwidth interconnect, the manifest must specify the required network speed: `HAS-SETUP-NIC-25G`, `HAS-SETUP-NIC-40G`, `HAS-SETUP-NIC-100G`, `HAS-SETUP-HUGEPAGE-2048kB-2048`, `HAS-SETUP-DPDK`.<br>See also: [Network Setup][Network Setup]. |
| `HAS-SETUP-DATASET` | This set of labels specifies the available dataset on the host.<br>See also: [Dataset Setup][Dataset Setup]. |
| `HAS-SETUP-DISK-SPEC` | This set of labels specify that SSD or NVME disks be mounted on the worker node(s).<br>See also: [Storage Setup][Storage Setup]. |
| `HAS-SETUP-BKC` | This set of labels specify the platform BKC version.<br>See also: [BKC Setup][BKC Setup]. |
| `HAS-SETUP-MODULE` | This set of labels specify the kernel modules that the workload must use.<br>See also: [Module Setup][Module Setup]. |
| `HAS-SETUP-HUGEPAGE` | This set of labels specify the kernel hugepage settings.<br>See also: [Hugepage Setup][Hugepage Setup] |
| `HAS-SETUP-GRAMINE-SGX` | This label specifies the SGX is enabled and GRAMINE software is installed on the system.<br>See also: [Gramine-SGX Setup][Gramine-SGX Setup] |
| `HAS-SETUP-FLEXRAN` | This set of label specifies the software and bios settings must be installed and configured on the system to run Flexran workload. Use the following labels: `HAS-SETUP-CENTOS7`, `HAS-SETUP-KERNEL-RT-3-10`, `HAS-SETUP-ACC100`.<br>See also: [FlexRan Setup][FlexRan Setup]. |
| `HAS-SETUP-CDN` | This set of labels specify cdn settings.<br>See also: [CDN Setup][CDN Setup] |
| `HAS-SETUP-HABANA-GAUDI` | This set of labels specify that the Habana AI accelerator is enabled.<br>See also: [Habana Setup][Habana Setup] |
| `HAS-SETUP-INFERENTIA-NEURON` | This set of labels specify that the AWS Inferentia NEURON accelerator is enabled.<br>See also: [AWS Inferentia NEURON Setup][AWS Inferentia NEURON Setup] |
| `HAS-SETUP-PVC` | This set of labels specify that the Intel® Data Center GPU Max Series (PVC) is enabled.<br>See also: [PVC Setup][PVC Setup] |
| `HAS-SETUP-NVIDIA-CUDA` | This set of labels specify that the AWS NVIDIA CUDA accelerator is enabled.<br>See also: [AWS NVIDIA CUDA Setup][AWS NVIDIA CUDA Setup] |
| `HAS-SETUP-SMART-DEK` | This label specifies that the Smart Edge Open Developer Experience Kits must be installed and configured on the system. Any workload that uses the Smart Edge Environment must specify this label. <br>See also: [Smart Edge Open DEK Setup][Smart Edge Open DEK Setup]. |
| `HAS-SETUP-5G` | This label specifies that the HW & SW config for build up the 5G environment is enabled.<br>See also: [5G Setup][5G Setup]. |
| `HAS-SETUP-CALICO-VPP-VCL` | This label specifies that the Calico VPP must be installed and VCL must be enabled meanwhile.<br>See also: [Calico VPP VCL Setup][Calico VPP VCL Setup]. |
| `HAS-SETUP-ADL-BKC` | This set of labels specifies the BKC settings for adl platform.<br>See also: [ADL Setup][ADL Setup] |
| `HAS-SETUP-MTL-BKC` | This set of labels specifies the BKC settings for mtl platform.<br>See also: [MTL Setup][MTL Setup] |
| `HAS-SETUP-NETWORK-SPEC` | This set of labels specify that special network to be set for the worker node(s).<br>See also: [Network Setup][Network Setup]. |
| `HAS-SETUP-RDMA` | This label specify that RDMA environement for network to be set for the worker node(s).<br>See also: [RDMA Setup][RDMA Setup]. |
| `HAS-SETUP-INTEL-ACM` | This label specifies that the intel ACM GPU HW device must be installed for the worker node(s). |
| `HAS-SETUP-INTEL-ATSM` | This label specify that Intel® Data Center GPU Flex Series should be setup and configured on the worker node(s).<br>See also: [ATSM Setup][ATSM Setup]. |
| `HAS-SETUP-INTEL-ARC` | This label specify that Intel® Arc™ Graphics should be setup and configured on the worker node(s).<br>See also: [Arc Setup][Arc Setup]. |
| `HAS-SETUP-VSI-HANTRO` | This label specify that Intel® Media IP and VSI Hantro driver should be setup and configured on the worker node(s) This is a Co-processor only available on several certain platforms.<br>See also: [Hantro Setup][Hantro Setup]. |
The label value is either `required` or `preferred` as follows:

```yaml
cluster:
- labels:
    HAS-SETUP-QAT-V170: required
    HAS-SETUP-NIC-40G: required
    HAS-SETUP-NIC-100G: preferred
    HAS-SETUP-HUGEPAGE-2048kB-2048: required
    HAS-SETUP-DPDK: required
```

## cluster.cpu_info

The `cluster.cpu_info` section describes any CPU-related constraints that a workload must use. The `cpu_info` section is currently declarative and is not enforced.

```yaml
cluster:
- cpu_info:
    flags:
    - "avx512f"
```

where the CPU flags must match what are shown by `lscpu` or `cat /proc/cpuinfo`.

## cluster.mem_info

The `cluster.mem_info` section describes any memory constraints that a workload must use. The `mem_info` section is currently declarative and is not enforced.

> Please also use the Kubernetes [resource constraints][resource constraints] to specify the workload memory requirements.)

```yaml
cluster:
- mem_info:
    available: 128
```

where the available memory is in the unit of GBytes.

## cluster.vm_group

The `cluster.vm_group` section describes the worker group that this worker node belongs to. Each worker group is a set of SUTs of similar specification. If not specified, the worker group is assumed to be `worker`.

> Enforced by the terraform backend.

```yaml
cluster:
- labels: {}
  vm_group: client
```

## cluster.off_cluster

The `cluster.off_cluster` section describes whether the worker node should be part of the Kubernetes cluster. This is ignored if the workload is not a Cloud Native workload or the execution is not through Kuberentes.

```yaml
cluster:
- labels: {}
- labels: {}
  off_cluster: true
```

If not specified, all nodes are part of the Kubernetes cluster.

## cluster.sysctls

The `cluster.sysctls` section describes the sysctls that the workload expects to use. The sysctls are specified per worker group. Multiple sysctls are merged together and applied to all the worker nodes in the same workgroup.

> Enforced by the terraform backend.

```yaml
cluster:
- labels: {}
  sysctls:
    net.bridge.bridge-nf-call-iptables: 1
```

## cluster.sysfs

The `cluster.sysfs` section describes the `sysfs` or `procfs` controls that the workload expects to use. The controls are specified per worker group. Multiple controls are merged together and applied to all the worker nodes in the same workgroup.

> Enforced by the terraform backend.

```yaml
cluster:
- labels: {}
  sysfs:
    /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor: performance
```

### cluster.bios

The `cluster.bios` section describes the bios settings that the workload expects to use. The controls are specified per worker group. Multiple controls are merged together and applied to all the worker nodes in the same workgroup.

> Enforced by the terraform backend.

```
cluster:
- labels: {}
  bios:
    SE5C620.86B:
      "Intel(R) Hyper-Threading Tech": Enabled          # Disabled
      "CPU Power and Performance Policy": Performance   # "Balanced Performance", "Balanced Power", or "Power"
```

### cluster.msr

The `cluster.msr` section describes the msr register settings that the workload expects to use. The controls are specified per worker group. Multiple controls are merged together and applied to all the worker nodes in the same workgroup.

> Enforced by the terraform backend.

```
cluster:
- labels: {}
  msr:
    0x0c90: 0x7fff
    0x0d10: 0xff
```

## terraform

The `terraform` section overwrites the default configuration parameters of the terraform validation backend default. See [Terraform Options][Terraform Options] for specific options.

```yaml
terraform:
  k8s_cni: flannel
```

> Note that any specified options in `TERRAFORM_OPTIONS` or by the CLI takes precedent. They will not be overriden by the parameters specified in this section.

### Example of Enabling Kubernetes NUMA Controls

```yaml
terraform:
  k8s_kubeadm_options:
    KubeletConfiguration:
      cpuManagerPolicy: static
      systemReserved:
        cpu: 200m
      topologyManagerPolicy: single-numa-node
      topologyManagerScope: pod
      memoryManagerPolicy: Static
      reservedMemory:
        - numaNode: 0
          limits:
            memory: 100Mi
      featureGates:
        CPUManager: true
        TopologyManager: true
        MemoryManager: true
```

### Example of Enabling Kubernetes Per-Socket Topology Aware Controls

Below configuration enables topology aware scheduling - including hardware cores and socket awareness. Only integral values for CPU reservations are allowed and misconfiguration of k8s deployment will result in SMTAlignmentError. This should be considered advanced users only example. Required Kubernetes version of 1.26.1 or higher.

```yaml
terraform:
  k8s_kubeadm_options:
    KubeletConfiguration:
      cpuManagerPolicy: static
      cpuManagerPolicyOptions:
        align-by-socket: "true"
        distribute-cpus-across-numa: "true"
        full-pcpus-only: "true"
      systemReserved:
        cpu: 1000m
      topologyManagerPolicy: best-effort
      topologyManagerPolicyOptions:
        prefer-closest-numa-nodes: "true"
      topologyManagerScope: pod
      memoryManagerPolicy: Static
      reservedMemory:
        - numaNode: 0
          limits:
            memory: 100Mi
      featureGates:
        CPUManager: true
        CPUManagerPolicyAlphaOptions: true
        CPUManagerPolicyBetaOptions: true
        CPUManagerPolicyOptions: true
        MemoryManager: true
        TopologyManager: true
        TopologyManagerPolicyAlphaOptions: true
        TopologyManagerPolicyBetaOptions: true
        TopologyManagerPolicyOptions: true
```

[QAT In-Tree Setup]: ../../user-guide/preparing-infrastructure/setup-qat-in-tree.md
[QAT Out-Of-Tree Setup]: ../../user-guide/preparing-infrastructure/setup-qat-out-of-tree.md
[DSA Setup]: ../../user-guide/preparing-infrastructure/setup-dsa.md
[IAA Setup]: ../../user-guide/preparing-infrastructure/setup-iaa.md
[DLB Setup]: ../../user-guide/preparing-infrastructure/setup-dlb.md
[Network Setup]: ../../user-guide/preparing-infrastructure/setup-network.md
[Storage Setup]: ../../user-guide/preparing-infrastructure/setup-storage.md
[BKC Setup]: ../../user-guide/preparing-infrastructure/setup-bkc.md
[Module Setup]: ../../user-guide/preparing-infrastructure/setup-module.md
[Hugepage Setup]: ../../user-guide/preparing-infrastructure/setup-hugepage.md
[Gramine-SGX Setup]: ../../user-guide/preparing-infrastructure/setup-gramine-sgx.md
[FlexRan Setup]: ../../user-guide/preparing-infrastructure/setup-flexran.md
[CDN Setup]: ../../user-guide/preparing-infrastructure/setup-cdn.md
[Habana Setup]: ../../user-guide/preparing-infrastructure/setup-habana.md
[AWS Inferentia NEURON Setup]: ../../user-guide/preparing-infrastructure/setup-inferentia.md
[PVC Setup]: ../../user-guide/preparing-infrastructure/setup-pvc.md
[AWS NVIDIA CUDA Setup]: ../../user-guide/preparing-infrastructure/setup-nvidia.md
[Smart Edge Open DEK Setup]: ../../user-guide/preparing-infrastructure/setup-smart-dek.md
[5G Setup]: ../../user-guide/preparing-infrastructure/setup-5g.md
[Calico VPP VCL Setup]: ../../user-guide/preparing-infrastructure/setup-calico-vpp-vcl.md
[ADL Setup]: ../../user-guide/preparing-infrastructure/setup-adl.md
[MTL Setup]: ../../user-guide/preparing-infrastructure/setup-mtl.md
[resource constraints]: https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource
[Terraform Options]: ../../user-guide/executing-workload/terraform-options.md#ansible-configuration-parameters
[DLB Setup]: ../../user-guide/preparing-infrastructure/setup-dlb.md
[Network Setup]: ../../user-guide/preparing-infrastructure/setup-network.md
[Dataset Setup]: ../../user-guide/preparing-infrastructure/setup-dataset.md
[Memory Setup]: ../../user-guide/preparing-infrastructure/setup-memory.md
[RDMA Setup]: ../../user-guide/preparing-infrastructure/setup-rdma.md
[ATSM Setup]: ../../user-guide/preparing-infrastructure/setup-atsm.md
[Arc Setup]: ../../user-guide/preparing-infrastructure/setup-arc.md
[Hantro Setup]: ../../user-guide/preparing-infrastructure/setup-hantro.md