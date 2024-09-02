# BKC Setup

Certain workloads require specific platform BKC version for optimal performance. Please install the BKC as specified and label the worker nodes.

## BKC image installation

The BKC image below currently used for NVR & AI Box workload (2023WW40.1'23) execution and development is MTL-P/PS: [MTL Ubuntu BSP Release Candidate - WW40.1'23 ER14 (MTL-U/H Beta RC01 & MTL-PS Alpha RC01)][MTL-U/H Beta RC01 & MTL-PS Alpha RC01]

### Checklist

- for NVR MTL-P/PS platform:
    - 4x4K monitor is connected and have display. for dummy HDMI/DP, make sure it's detected and able to render.
    - RAM is connected with 32GB (2x16GB DDR5 5600 MT/s [5600 MT/s]).
    - RTSP server (if required) connection to SUT should be in local network

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
## OpenVINO-FIS Workload Execution Environment Setup

Acoording to [Steps to prepare MeteorLake environment](https://github.com/intel-sandbox/bmk_openvino/tree/dev24.04?tab=readme-ov-file#steps-to-prepare-meteorlake-environment)

1. From ubuntu 22.04 install linux kernel 6.7.1
    https://kernel.ubuntu.com/mainline/v6.7.1/amd64/
    download these 4 deb ，
    - linux-headers-xxx.deb
    - linux-headers-xxx_all.deb
    - linux-image-xxx.deb
    - linux-module-xxx.deb
   ```bash
   sudo dpkg -i *deb
   sudo apt install -f
   ```

2. Download mtl firmware
   ```bash
   git clone https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/
   cd linux-firmware/i915
   sudo mv mtl_* /lib/firmware/i915/
   ```

3. Reboot computer
   ```bash
   if everything works, we should see /dev/dri/renderD128 device
   ll /dev/dri/renderD128
   crw-rw----+ 1 root render 11:12 /dev/dri/renderD128
   ```

4. install npu driver https://github.com/intel/linux-npu-driver/releases

## Node Labels:

Label the worker nodes with the following node labels:
- `HAS-SETUP-MTL-BKC=yes`


[MTL-U/H Beta RC01 & MTL-PS Alpha RC01]: https://wiki.ith.intel.com/pages/viewpage.action?pageId=3202154828