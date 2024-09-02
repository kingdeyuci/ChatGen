# <table><tbody><tr><td><img src="https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features/wiki/image/service-framework-logo.png" width=192 height=96></td><td>Workload Services Framework &mdash; Intel Internal </td></tr></table>

### Introduction

This is the **Workload Services Framework** Intel internal repository. The repo contains hero-feature workloads for multiple platforms. Each workload is a complete and standalone implementation that can be built and run collectively or individually. See the list of supported workloads under the [workload](https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features/tree/master/workload#readme) directory.  

<p align="center"><img src="doc/image/wsf-pipeline.svg" width="90%"></p>
  
<details>
<summary>

### Quick Navigation

</summary>

  - [Setup Environment](#setup-environment)
  - [Evaluate Workload](#evaluate-workload)
  - [Build Workload](#build-workload)
  - [Developer Guide](#see-also)
  - [Contributing Guide](CONTRIBUTING.md)  
  - [Report Bugs](https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features/issues)  
  - [Discussion Forum](https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features/discussions)  
  - [Announcements](https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features/discussions/categories/announcements)  
  - [Releases](https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features/releases)  
  - [Frequently Asked Questions](https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features/wiki/FAQ)  
  
</details>

### Setup Environment

- Sync your system date/time. This is required by any credential authorization.  
- If you are behind a corporate firewall, please setup `http_proxy`, `https_proxy` and `no_proxy` in `/etc/environment`.
- Run the [`setup-dev.sh`](doc/user-guide/preparing-infrastructure/setup-wsf.md#setup-devsh) script to setup the development host for Cloud and On-Premises workload development and evaluation. See [Cloud](#doc/user-guide/preparing-infrastructure/setup-wsf.md#cloud-setup) and [On-Premises](doc/user-guide/preparing-infrastructure/setup-wsf.md#on-premises-setup) Setup for more details on additional setup steps.
  
### Evaluate Workload

You can use any official [releases](https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features/releases) for workload evaluation.

```
mkdir build 
cd build
git checkout 24.04.2
cmake -DRELEASE=v24.04.2 -DBENCHMARK=BoringSSL ..     # .. is required here
make                                    # Optional step to build the workload
./ctest.sh -N                           # List all test cases
./ctest.sh -R _pkm -V                   # Evaluate a specific test case
./list-kpi.sh workload/BoringSSL/logs*  # Show KPIs
```

---

- It is critical to keep github codebase and rebuilt images in sync. The `git checkout 24.04.2` and `cmake -DRELEASE=v24.04.2 ..` ensure that the prebuilt images work with the github codebase they compiled with. Replace `v24.04.2` with the release version of interest.   

- The `cmake -DBENCHMARK=dummy ..` step restricts the build and evaluation to the dummy workload. You can change to the name of any [supported](workload/README.md) workload. 

- If you use the official release, the `make` step is not required. The build step is skipped to use the official release images.  

- `./ctest.sh` is used to evaluate a workload. Different workload usage scenarios (and their configuration parameters) are described as test cases. You can list the testcases with `-N` and select a testcase or a subset of testcases with `-R`. See [`ctest.md`](doc/user-guide/executing-workload/ctest.md) for more details.

- `./list-kpi.sh` is used to format workload output into a list of key/value pairs. You can also use `./list-kpi.sh` for simple analysis and to create EXCEL spreadsheets. See [`ctest.md`](doc/user-guide/executing-workload/ctest.md#list-kpish) for more details.

- The WSF supports multiple validation backends. By default, the [`terraform`](doc/user-guide/preparing-infrastructure/setup-terraform.md) backend is used to valuate workloads on Cloud or on-premises. You can choose alternative backends such as [`docker`](doc/user-guide/preparing-infrastructure/setup-docker.md) and [`kubernetes`](doc/user-guide/preparing-infrastructure/setup-kubernetes.md), each of which supports a subset of the usage scenarios For example, the `docker` backend can be used to run single-container workload on your development machine, mostly used for simple workload development.

---

### Build Workload

If you need to build the workload(s), create a [`~/.netrc`](workload/README.md#access-permission) file with `github/gitlab` access tokens. See the [workload table](workload/README.md#list-of-workloads) for workload specific permission requirements.

You need to additionally specify the `REGISTRY` value, which can be an empty value most of the time except in the case of On-Premises Kubernetes validation.  

> If the `REGISTRY` value is not empty, any re-built docker images will be pushed to the specified docker registry. Please `docker login` beforehand if the docker registry requires authentication.   

```
mkdir -p build
cd build
cmake -DREGISTRY= -DBENCHMARK=ResNet-50 ..  # Optionally specify -DPLATFORM=SPR
make                                        # Build the workload
./ctest.sh -N                               # List all test cases
./ctest.sh -V -R <test-case-name>           # Execute a specific test case
./list-kpi.sh workload/ResNet-50/logs*      # Show KPIs
```

### See Also

- [Build Options](doc/user-guide/executing-workload/cmake.md)
- [Test Options](doc/user-guide/executing-workload/ctest.md)
- [Develop New Workload](doc/developer-guide/component-design/workload.md)
- [Develop New Software Stack](doc/developer-guide/component-design/stack.md)
- [Develop New VM Image](doc/developer-guide/component-design/image.md)
