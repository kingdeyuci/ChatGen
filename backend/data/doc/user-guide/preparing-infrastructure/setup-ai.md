This document's contents is deprecated and may not update any more. please refer to the latest contents from [wiki](https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features/wiki/Getting-started-with-AI-workloads-in-WSF) now.

# Setup AI

This document is a guide for using AI workload.

## AI Workload Naming

Any AI workload should follow the naming convention: `<Model Name>-<Framework>-<Platform>-<Additions>` e.g. `BERTLarge-PyTorch-Xeon-Public`.

`<Platform>` might be ignored if it is `Xeon`.

- **Model Name**: Specify AI deep learning Model Name
- **Framework**: Specify one of the available frameworks
    - `TensorFlow`
    - `PyTorch`
    - `OpenVINO` (Intel CPU only)
    - `TensorRT` (Nvidia GPU only)
- **Platform**: Specify one of the available platforms
    - `''` (empty for Intel Xeon CPU)
    - `EPYC` (AMD EPYC CPU)
    - `ARM`/`ARMv8`/`ARMv9` (ARM based CPU)
    - `Nvidia` (Nvidia GPU)
    - `Inferentia` (AWS inference accerlator card)
    - `PVC` (Intel Data Center GPU Max series)
    - `Gaudi` (Gaudi or Gaudi2)
- **Additions**: Specify additional information for the workload.
    - One typical information in `Additions` is `Recipe Types`:
        - `Public`: Intel recommended recipe with Intel optimization and full stack is public available.
        - `Dev`: Intel recommended recipe with Intel optimization, which is still under development and not public available yet. For example, Dev recipes for pre-PRQ systems.
        - `OOB`: Out of Box recipe. It is with default configuration when user installs SW stack from original web sites, which is usually HW agnostic. So it might not come with Intel recommended optimization by default. It is usually the first impression/experience that user gets when workload becomes available to public initially. The full stack is also public available.

## AI Testcase Naming

```text
<WL name>_inference_throughput_gated
<WL name>_inference_throughput_pkm
<WL name>_inference_latency
<WL name>_inference_accuracy
<WL name>_training_throuphput
<WL name>_training_accuracy
```



## Configuration

Any AI workload can be run on bare metal and cloud VMs. AWS, GCP and Azure cloud are recommended.

Suggested cloud instance type:

### Intel ICX

- AWS cloud: `m6i`
- GCP cloud: `n2-highmem-96`
- Azure cloud: `Dv5-series`

### AMD Milan

- AWS cloud: `m6a`
- Azure cloud: `Dasv5` and `Dadsv5-series`

### AMD Roma

- AWS cloud: `m5a`
- Azure cloud: `Dav4` and `Dasv4-series`

### AWS Graviton2

- AWS cloud: `m6g`

### AWS Graviton3

- AWS cloud: `c7g`

### AWS Inferentia

- AWS cloud: `inf`

### Nvidia GPU

- AWS cloud: `g4dn` (T4)


### Best Configuration

- **For AI workloads executed on ICX platforms**:
[Tuning Guide for Deep Learning on 3rd Gen][Tuning Guide for Deep Learning]
- **For AI workloads executed on SPR platforms**:
[Tuning Guide for Deep Learning on 4th Gen][Tuning Guide for Deep Learning 4th gen]


### Node Labels

Setup the following node labels for AI workloads:

- `HAS-SETUP-BKC-AI=yes` (optional)


### KPI output

KPI output example:

```text
#================================================
#Workload Configuration
#================================================
##FRAMEWORK: PyTorch 1.13.0a0+gitd7607bd
##MODEL_NAME: DLRM
##MODEL_SIZE: 89137319
##MODEL_SOURCE: Facebook
##DATASET: Criteo 1TB Click Logs (terabyte)
##FUNCTION: inference
##MODE: throughput
##PRECISION: avx_fp32
##DATA_TYPE: real
##BATCH_SIZE: 1
##STEPS: 1
##INSTANCE_NUMBER: 2
##CORES_PER_INSTANCE: 56
#================================================
#Application Configuration
#================================================
##SCENARIO: offline
##SERVING_STACK: -
##MODEL_WORKERS: -
##REQUEST_PER_WORK: -
#================================================
#Metrics
#================================================
Average Throughput (samples/sec): 27168.18
Max Latency (ms): -1
Min Latency (ms): -1
Mean Latency (ms): 4.33
P50 Latency (ms): -1
P90 Latency (ms): -1
P95 Latency (ms): -1
P99 Latency (ms): -1
P999 Latency (ms): -1
TTT: -1
Samples: -1
Compute Utilization: -1
Memory Utilization: 89.79 GB
FLOPs: -1
Model Quality Metric Name: -1
Model Quality Value: -1
Cost Per Million Inferences: -1
#================================================
#Key KPI
#================================================
*Throughput (samples/sec): 27168.18
```

## AI big image solution

Big image solution means dataset image and benchmark image are decoupled. Dataset image must be prepared before case execution, Or you'll get error log similarly:
```
Dataset not available at /opt/dataset/**. This workload is enabling big image solution. Please prepare dataset first according to README.
```
### BM preparasion for large dataset and model
1. Run cmake cmdline

```
cmake -DREGISTRY=xx.xx.xx.xx:20666 -DBACKEND=terraform -DTERRAFORM_OPTIONS="--owner=xxx" -DTERRAFORM_SUT=static -DBENCHMARK= ..
```

> Note:  `-DBACKEND` option MUST be `terraform` because there are part of auto-provisioning to check dataset readiness and add Label in terraform.

2. Build  Dataset images

2.1. Switch to dataset folder

```
cd {{Your WSF_HOME}}/build/image/dataset-ai/
```

2.2. Build image to prepare your dataset/model to BM. Please get dataset name for each workload from workload Readme and replace below `XXX`.

```
make build_dataset_ai_XXX
```

### CSP VM image preparasion for large dataset and model
1. Run cmake cmdline

```
cmake -DREGISTRY=xx.xx.xx.xx:20666 -DBACKEND=terraform -DTERRAFORM_OPTIONS="--owner=xxx" -DTERRAFORM_SUT=aws/gcp/alicloud/azure -DBENCHMARK= ..
```
> Note:  `-DBACKEND` option MUST be `terraform` because there are part of auto-provisioning to check dataset readiness and add Label in terraform.

2. Build  Dataset images if there are no dataset in the CSP region
2.1. Switch to dataset folder
```
cd {{Your WSF_HOME}}/build/image/dataset-ai/
```

2.2. Build image to prepare your dataset/model on csp. Please get dataset name for each workload from workload Readme and replace below `XXX`.

```
make build_dataset_ai_XXX
```

> Please skip `Step 2` if you want to run AI on below CSP zones. AI big images dataset are ready on them:
```
aws: us-west-2a
gcp: us-west1-a
alicloud: cn-beijing-a/cn-shanghai-m
azure: eastus-1
```

**NOTE**: Make sure gprofiler telemetry data is accurate. You need to use the `_pkm` case or set a larger `STEPS`.


[testcase.md]: https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features/blob/master/doc/user-guide/executing-workload/testcase.md
[Tuning Guide for Deep Learning]: https://www.intel.com/content/www/us/en/developer/articles/guide/deep-learning-with-avx512-and-dl-boost.html
[Tuning Guide for Deep Learning 4th gen]: https://www.intel.com/content/www/us/en/developer/articles/guide/deep-learning-avx512-and-dl-boost-4th-gen-xeon.html