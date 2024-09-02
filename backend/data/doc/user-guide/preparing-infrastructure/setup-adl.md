# BKC Setup

Certain workloads require specific platform BKC version for optimal performance. Please install the BKC as specified and label the worker nodes.

## BKC image installation

The BKC image below currently used for NVR & AI Box workload (2022WW49.5) execution and development is ADL-S/P/N: [ADL-S/P/N: Base Ubuntu release - 2023WW08][ADL-S/P/N: Base Ubuntu release - 2023WW08]

### Checklist

- for NVR ADL-P/S/PS platform:
    - 4x4K monitor is connected and have display. for dummy HDMI/DP, make sure it's detected and able to render.
    - RAM is connected with 2x16GB with 4800MHz
    - RTSP server (if required) connection to SUT should be in local network
- for NVR ADL-N platform
    - 2x4K monitor is connected and have display. for dummy HDMI/DP, make sure it's detected and able to render.
    - RAM is connected with 1x32GB with 4800MHz
    - RTSP server (if required) connection to SUT should be in local network
- for iNVR
    - 1x4k monitor is connected and have display.

## NVR Workload Execution Environment Setup

1. Set the permission to be able to access the docker daemon.
    ```shell
    sudo usermod -aG docker user
    sudo chmod 666 /var/run/docker.sock
    ```
2. Setup certificate for harbor access:
    - download from the code repository and run the `ca_install.sh` script, then restart docker service
        ```shell
        wget --no-proxy https://af01p-png.devtools.intel.com/artifactory/edge_system-png-local/NVR/ZTA_Utils/ca_install.sh
        ./ca_install.sh
        ```
3. Export display
    ```shell
    wget --no-proxy https://af01p-png.devtools.intel.com/artifactory/edge_system-png-local/NVR/ZTA_Utils/display_export.sh
    ./display_export.sh
    ```

## RTSP server setup (optional)

All proxy workloads are using file source as input streams. Some customized workload (or you intend to change to) use RTSP source, the below is to setup RTSP server for input streams. Required a dedicated setup (CML SKU and above) with Ubuntu 22.04 and Docker.io installed. In addition, the RTSP server needs to be installed on a machine outside the SUT, and the network is reachable.

1. Setup certificate for harbor access:
    - download from the code repository and run the `ca_install.sh` script, then restart docker service
        ```shell
        wget --no-proxy https://af01p-png.devtools.intel.com/artifactory/edge_system-png-local/NVR/ZTA_Utils/ca_install.sh
        ./ca_install.sh
        ```
2. Pull the NVR RTSP server container
    ```shell
    docker pull gar-registry.caas.intel.com/virtiot/rtspsvr:nvr-ww43.1
    ```
3. Run the RTSP server
    ```shell
    docker run -it --rm --privileged -d -p 8554:8554 -p 8555:8555 gar-registry.caas.intel.com/virtiot/rtspsvr:nvr-ww43.1
    ```

## Node Labels:

Label the worker nodes with the following node labels:
- `HAS-SETUP-ADL-BKC=yes`


[ADL-S/P/N: Base Ubuntu release - 2023WW08]: https://wiki.ith.intel.com/pages/viewpage.action?pageId=2788293670