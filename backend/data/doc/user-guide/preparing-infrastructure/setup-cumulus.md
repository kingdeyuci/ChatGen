
# Cumulus Setup

The cumulus backend can be used to validation workloads on a remote cluster, On-Premises or on Cloud. 

## Prerequisite

- If you just want to evaluate released workloads (without build), 

  - Set the value of the `REGISTRY` cmake variable to be `amr-registry.caas.intel.com/sf-cwr`. This points to a read-only docker registry where the released workload images and cumulus docker images are preloaded. You might want to additional specify the `RELEASE` value to point to a specific release version.   

  ```shell
  cmake -DBACKEND=cumulus -DREGISTRY=amr-registry.caas.intel.com/sf-cwr -DRELEASE=v22.18 ..
  ```

- If you plan to build any workloads from scratch, 

  - Setup a [`~/.netrc`][netrc] file so that the build script can access to the [cumulus][cumulus] repository.
  - Set the `REGISTRY` cmake variable to point to a [private][private] docker registry where you have write permission.

  ```
  cd build
  cmake -DBACKEND=cumulus -DREGISTRY=<registry-url> ..
  make build_cumulus
  ```

## Setup Cumulus for Cloud Validation

The cumulus backend supports Cloud vendors such as `AWS`, `GCP`, `AZURE`, `Tencent`, and `AliCloud`. Each vendor has a corresponding configuration file: `script/cumulus/cumulus-config.<SUT>.yaml`, where `<SUT>` is the Cloud vendor name. You can customize as needed.  

### Configure Cloud Account

```
make aws           # or make -C ../.. aws, if under build/workload/<workload>
$ aws configure    # please specify a region
$ exit
```

```
make azure         # or make -C ../.. azure, if under build/workload/<workload>
$ az login
$ exit
```

```
make gcp           # or make -C ../.. gcp, if under build/workload/<workload>
$ gcloud init --no-browser
$ exit
```

```
make tencent       # or make -C ../.. tencent, if under build/workload/<workload>
$ tccli configure  # please specify a region
$ exit
```

```
make alicloud      # make -C ../.. alicloud, if under build/workload/<workload>
$ aliyun configure # please specify a region
$ exit
```

### Run Workload(s) Through Cumulus

```
cd workload/<workload>
make
./ctest.sh -N
```

### Cleanup Cloud Resources

If your cumulus validation is interrupted for any reason, the Cloud resource may remain active. You can explicitly cleanup any Cloud resources as follows:

```
make -C ../.. aws
$ cleanup
$ exit
```

```
make -C ../.. gcp
$ cleanup
$ exit
```

```
make -C ../.. azure
$ cleanup
$ exit
```

```
make -C ../.. tencent
$ cleanup
$ exit
```

```
make -C ../.. alicloud
$ cleanup
$ exit
```

### Use A Cloud Private Registry

A Cloud private registry is a convenient option to store workload images. During the Cloud validation, the SUTs (System Under Test) can directly pull images from the docker registry without transfering any images. Here we assume the Cloud registry and the SUTs are in the same region.  

Add the following flag in the `flags` section of `script/cumulus/cumulus-config.<cloud>.yaml` to indicate that the SUTs can directly access to the registry. The cumulus backend will then skip transfering workload images during validation:  

```
  flags:
    skopeo_sut_accessible_registries: "<registry-url>"
```

See Also: [Private Registry Authentication][Private Registry Authentication]

## Setup Cumulus for On-Premises Validation


- Follow the instructions in the [WSF On-Premises Setup][WSF On-Premises Setup] to setup the On-Premises hosts.
- Customize [`cumulus-config.static.yaml`][cumulus-config.static.yaml] to specify your cluster information.
- Run any workload through cumulus:    

```
cd workload/<workload>
make
./ctest.sh -N
```

## Cumulus Options

Use the following options to customize the cumulus validation:  
- Publish the validation results to the cumulus [dashboard][dashboard]:

  ```
  cmake -DCUMULUS_OPTIONS="--intel_publish" ..
  ```

- Specify the tester name. By default, the tester is your user name:

  ```
  cmake -DCUMULUS_OPTIONS=--owner=mytester ..
  ```

- Set the default to use `docker` in validation wherever possible:  

  ```
  cmake -DCUMULUS_OPTIONS=--docker-run ..
  ```

- Set the dry-run mode. Configure the workload but skip the execution stage: 

  ```
  cmake -DCUMULUS_OPTIONS=--dry-run ..
  ```

## Enabling powerstat traces for your workload
### Requirements

* Running ODMS 0.3.0 with ipmi-exporter and telegraf including powerstat plugin enabled
* Prometheus metrics endpoint available for SF

### How to use

To enable gathering powerstat data run workload passing following arguments:
* `--powerstat` (bool) to `CUMULUS_OPTIONS`
to enable gathering of power metrics
* `--powerstat_prometheus_url` (string) to `CUMULUS_OPTIONS`.
URL to prometheus API

## Telemetry Tracing

Note: `emon` is not supported for On-Cloud validation

You can enable telemetry tracing via `sar`, `emon`, and/or `collectd` as follows:  
- **`sar`**: Add `--sar` to `CUMULUS_OPTIONS`.  
- **`emon`**: Add `--emon --edp_publish --emon_post_process_skip` to `CUMULUS_OPTIONS`.  
- **`collectd`**: Add `--collectd` to `CUMULUS_OPTIONS`.  

  ```
  cmake -DCUMULUS_OPTIONS=--collectd ..
  cd workload/<workload>
  ./ctest.sh -N
  ```

For On-Cloud validation, there is no additional setup. For On-Premises validation, you need to perform additional setup for each telemetry tracing mechanism: 

### Setup `sar` On-Prem

- Install the `sar` utility on your worker nodes. 

### Setup `EMON` On-Prem

On your worker nodes,
- Install `python3`, `xlswriter` and `ruby`.  
- Create a `/opt/pkb` folder with the right ownership:  

  ```
  sudo mkdir -p /opt/pkb
  sudo chown $(id -u):$(id -g) /opt/pkb
  ```

- Download and install [EMON][EMON] to `/opt/emon/emon_files`.
> Note it is critical that the installation location is `/opt/emon/emon_files`.  
 
- Add your worker username to the `vtune` group.   

  ```
  sudo usermod -aG vtune $(id -gn)
  ```

### Setup Collectd On-Prem

On your worker nodes, 
- Install `flex`, `bison`, `autoconf`, `automake` and `libtool`.  
- Download [collectd][collectd] and compile it as follows:

  ```
  sudo mkdir -p /opt/pkb
  sudo chown -R $(id -u).$(id -g) /opt/pkb
  sudo mkdir -p /opt/collectd
  sudo chown -R $(id -u).$(id -g) /opt/collectd

  git clone https://github.com/collectd/collectd.git
  cd collectd
  ./build.sh
  ./configure --prefix=/opt/collectd/collectd
  make
  make install
  ```

- Copy [collectd.conf][collectd.conf] to `/opt/collectd/collectd/etc`.

### Experiment Manager

**NOTE: Experiment manager is deprecated and will no longer be supported.**

The cumulus backend interacts with the experiment manager plugin by using the `--experiment_manager` flag. Additionally, the following flags can be enabled:
- `--experiment_manager_kafka_broker`: The kafka broker to be used for the experiment.
- `--experiment_manager_start_topic`: Kafka topic to fetch the metadata during StartExperimentManager().
- `--experiment_manager_prepare_topic`: Kafka topic to push the metadata during PrepareExperimentManager().
- `--experiment_manager_stop_topic`: Kafka topic to push the metadata during StopExperimentManager().

The experiment manager plugin can be invoked from the build folder as follows:
```
cmake -DCUMULUS_OPTIONS="--experiment_manager --experiment_manager_kafka_broker=<KAFKA_BROKER>" ..
```

## Cumulus Debugging

Enable the cumulus debugging mode as follows:  

- Specify break points in `CUMULUS_OPTIONS`:  

  ```
  cmake -DCUMULUS_OPTIONS=--dpt_debug=<BreakPoint>[,<BreakPoint>] ..
  ```

where `<BreakPoint>` can be one of more of the following strings:  
- `PrepareStage`: Pause when the workload is about to setup the host environment. 
- `SetupVM`: Pause when the workload is about to setup external VMs. 
- `RunStage`: Pause when the workload is about to start the workload execution. 
- `CleanupStage`: Pause when the workload is about to cleanup.  
- `ScheduleExec`: Pause when the workload is about to schedule execution.
- `ExtractLogs`: Pause when the workload is about to extract logs. 
- `ExtractKPI`: Pause when the workload is about to parse KPIs. 

Start the workload validation as usual (`./ctest.sh`), cumulus will pause at the specified breakpoints. You can start a new shell and login to the cumulus container as follows:  

```
./debug.sh
$
```

Now you can `ssh` to the remote worker and start debugging. To resume validation, simply create an empty signalling file `Resume<BreakPoint>` under `/tmp/pkb/runs/<runid>/` as follows:  

```
> touch /tmp/pkb/runs/784d84f59e3d/ResumeRunStage
```

## See Also

- [Performance Tools][Performance Tools]
- [TCP TIME_WAIT Reuse][TCP TIME_WAIT Reuse]
- [Unsuitable CPU Speed Policy][Unsuitable CPU Speed Policy]
- [Cumulus Repository][Cumulus Repository]

[netrc]: ../../../workload/README.md#access-permission
[cumulus]: https://github.com/intel-innersource/frameworks.benchmarking.cumulus.perfkitbenchmarker
[private]: https://docs.docker.com/registry/deploying
[Private Registry Authentication]: setup-auth.md
[WSF On-Premises Setup]: setup-wsf.md#on-premises-development-setup
[cumulus-config.static.yaml]: ../../../script/cumulus/cumulus-config.static.yaml
[dashboard]: https://cumulus-dashboard.intel.com/services-framework
[EMON]: https://intel.sharepoint.com/sites/performance-tools
[collectd]: https://github.com/collectd/collectd
[collectd.conf]: ../../../script/cumulus/collectd.conf
[Performance Tools]: https://intel.sharepoint.com/sites/performance-tools
[TCP TIME_WAIT Reuse]: https://github.com/intel/Updates-for-OSS-Performance/blob/main/time_wait.md
[Unsuitable CPU Speed Policy]: https://github.com/intel/Updates-for-OSS-Performance/blob/main/cpufreq.md
[Cumulus Repository]: https://github.com/intel-innersource/frameworks.benchmarking.cumulus.perfkitbenchmarker

