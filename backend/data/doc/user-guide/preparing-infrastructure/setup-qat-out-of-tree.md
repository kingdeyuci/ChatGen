<!-- TODO: Further changes are necessary -->

# Setup QAT out-of-tree

Intel® QuickAssist Technology allows data encryption and compression. Out-of-tree setup for **4xxx** device is described in this document.

## System setup - only Physical Functions
- Disable `VT-d` in BIOS
    ```text
    EDKII Menu
    → Socket Configuration
      → IIO Configuration
        → Intel VT for directed IO (VT-d)
          → Intel VT for directed IO
            → Disable
    ```
- Disable IOMMU and setup hugepages from your kernel command line:
    ```shell
    sudo grubby --update-kernel=DEFAULT --args="intel_iommu=off default_hugepagesz=2M hugepagesz=2M hugepages=4096"
    ```
- Reboot your system for the kernel settings to take effect.


## System setup - both Physical and Virtual Functions
- Enable `VT-d` in BIOS:
    ```text
    EDKII Menu
    → Socket Configuration
      → IIO Configuration
        → Intel VT for directed IO (VT-d)
          → Intel VT for directed IO
            → Enable
    ```
-  Enable IOMMU and setup hugepages from your kernel command line:
    ```shell
    sudo grubby --update-kernel=DEFAULT --args="intel_iommu=on iommu=pt default_hugepagesz=2M hugepagesz=2M hugepages=4096"
    ```
- Reboot your system for the kernel settings to take effect.


## QAT 2.0 Driver Setup

Fedora:

```shell
# Install dependencies
sudo dnf config-manager --set-enabled powertools
sudo yum -y groupinstall "Development Tools" 
sudo yum -y install yasm pciutils libudev-devel openssl-devel boost-devel libnl3-devel 
sudo yum -y install kernel-next-server-devel
```

Ubuntu:

```shell
sudo apt update -y 
sudo apt install -y build-essential cmake g++ pkg-config wget make yasm nasm libboost-all-dev libnl-genl-3-dev zlib1g zlib1g-dev
apt install -y systemd m4 pkg-config libudev-dev libssl-dev autoconf libtool tar git libssl-dev
```


### Build and install 1.x QAT Drivers

```shell
# Ref: https://downloadmirror.intel.com/761891/README_QAT.L.4.20.0-00001.txt
wget https://downloadmirror.intel.com/761891/QAT.L.4.20.0-00001.tar.gz # Version: QAT.L.4.20.0-00001 (12-Dec-2022)
sudo mkdir -p /opt/intel/QAT
tar -xvzf QAT.L.4.20.0-00001.tar.gz -C /opt/intel/QAT
sudo ./configure
sudo make
sudo make -j install

# Make sure qat service is started properly and ready to use
sudo systemctl stop qat.service
sudo systemctl enable qat.service
sudo systemctl restart qat.service
sudo systemctl status qat.service
```

### Build and install 2.x QAT Drivers

```shell
# Ref: https://www.intel.com/content/www/us/en/download/765501/intel-quickassist-technology-driver-for-linux-hw-version-2-0.html
wget https://downloadmirror.intel.com/765523/QAT20.L.1.0.0-00021.tar.gz # Version: QAT20.L.1.0.0-00021 (10-Jan-2023)
sudo mkdir -p /opt/intel/QAT
tar -xvzf QAT20.L.1.0.0-00021.tar.gz -C /opt/intel/QAT
sudo ./configure
sudo make
sudo make -j install

# Make sure qat service is started properly and ready to use
sudo systemctl stop qat.service
sudo systemctl enable qat.service
sudo systemctl restart qat.service
sudo systemctl status qat.service
```
> To setup QAT VFs, need probe vfio-pci and change configuration:

```shell
cd /opt/intel/QAT
sudo modprobe vfio-pci disable_denylist=1
sudo ./configure --enable-icp-sriov=host
sudo make
sudo make -j install

# Make sure qat service is started properly and ready to use
sudo systemctl stop qat.service
sudo systemctl enable qat.service
sudo systemctl restart qat.service
sudo systemctl status qat.service
```

Optionally check the QAT driver features with sample code:

```shell
cd /opt/intel/QAT
sudo make samples-install
cd /usr/local/bin/
./cpa_sample_code 

# Make sure qat service is started properly and ready to use
sudo systemctl stop qat.service
sudo systemctl enable qat.service
sudo systemctl restart qat.service
sudo systemctl status qat.service
```

### Intel QATLibs Installation (Optional Requirement If Needed)
  
> **Note:** This package provides user space libraries that allow access to Intel QuickAssist devices and expose the Intel(R) QuickAssist APIs and sample codes.

```shell
git clone https://github.com/intel/qatlib.git
cd qatlib
./autogen.sh
./configure --enable-service
```
### OpenSSL*Engine Installtaion

```shell
# Before building OpenSSL*Engine need to build OpenSSL*Engine Libraries "ipp-crypto" & "intel-ipsec-mb" also

git clone https://github.com/intel/ipp-crypto.git
cd /ipp-crypto/sources/ippcp/crypto_mb && \
cmake . -B"../build" \
-DCMAKE_INSTALL_PREFIX=/usr && \
cd ../build && \
make -j crypto_mb && \
make install

git clone https://github.com/intel/intel-ipsec-mb.git
cd /intel-ipsec-mb && \
make -j SAFE_DATA=y SAFE_PARAM=y SAFE_LOOKUP=y && \
make install NOLDCONFIG=y

git clone https://github.com/intel/QAT_Engine
cd /QAT_Engine && \
./autogen.sh && \
./configure --enable-qat_sw && \
make && make install
```

Setup hugepages and install the modules and services:

```
echo 4096 | sudo tee /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
sudo rmmod usdm_drv
sudo insmod /opt/intel/QAT/build/usdm_drv.ko max_huge_pages=4096 max_huge_pages_per_process=224

# Make sure qat service is started properly and ready to use
sudo systemctl stop qat.service
sudo systemctl enable qat.service
sudo systemctl restart qat.service
sudo systemctl status qat.service
```

## QAT HW Build Package

> The QAT HW images must be built against a specific OS kernel version. The default is against the `next` kernel, version `5.12`. The corresponding Dockerfiles must be updated if the OS kernel version is different. Use the following command to generate the qat-driver package used in the Dockerfiles:    

```
sudo tar cvfz ~/qat-driver-20-$(uname -r).tar.gz -C / /opt/intel/QAT/build $(find /opt/intel/QAT -name '*.h') /etc/udev/rules.d/00-qat.rules
```

## QAT Driver Configuration

> The default QAT default configuration may not work for all use cases. Please see how to [replace the QAT driver config file][replace the QAT driver config file].

> The [`qat-invoke.sh`][qat-invoke.sh] script can be used to generate the QAT device configurations. Examples as follows:

```
SERVICES_ENABLED=asym SECTION_NAME=SHIM CY_INSTANCES=8 PROCESSES=8 qat-invoke.sh
```
```
SERVICES_ENABLED=sym SECTION_NAME=SHIM CY_INSTANCES=1 PROCESSES=64 qat-invoke.sh
```
```
SERVICES_ENABLED=asym SECTION_NAME=SSL CY_INSTANCES=8 PROCESSES=8 qat-invoke.sh
```
```
SERVICES_ENABLED=sym SECTION_NAME=SSL CY_INSTANCES=8 PROCESSES=8 qat-invoke.sh
```
```
SERVICES_ENABLED=dc SECTION_NAME=SSL DC_INSTANCES=1 PROCESSES=64 qat-invoke.sh
```

## Node Labels

> Label the QAT worker node(s) with the following node labels:  
- `HAS-SETUP-KERNEL-V0512=yes`: Must have.  
- `HAS-SETUP-CENTOS8=yes`: Must have.  
- `HAS-SETUP-QAT=yes`: Must have. 
- `HAS-SETUP-QAT-V200=yes`: Must have.  
- `HAS-SETUP-HUGEPAGE-2048kB-4096=yes`: Must have.  
An additional label is needed if QAT VF is required:
- `HAS-SETUP-MODULE-VFIO-PCI=yes`: Must have.

If needed, NFD-based labels can also be configured for Intel Device Plugins [doc/nfd-with-intel-device-plugins.md][doc/nfd-with-intel-device-plugins.md]

## QAT Driver / OpenSSL / OpenSSL*Engine Drivers Uninstall

> Remove the driver / configuration and clean-up. Especially helpful if QAT driver / OpenSSL / OpenSSL*Engine setup needs to be re-configured

```shell
sudo systemctl stop qat.service
# Move to dir location in which drivers / configuration are saved such as "/opt/intel/QAT" and execute mentioned below commands:
make uninstall
make clean
make distclean
```

## References

* NFD + Intel Device Plugins Labels: For more information on labels, please visit [setup-nfd.md][setup-nfd.md]
* For more information on setting up PFs / VFs for specific QAT devices, please visit - https://doc.dpdk.org/guides/cryptodevs/qat.html
* For more information about QAT, visit [QAT Developers page][QAT Developers page].

[replace the QAT driver config file]: https://gitlab.devtools.intel.com/qat_apps/qat_engine#copy-the-intel-quickassist-technology-driver-config-files-for-qat_hw
[qat-invoke.sh]: ../../../dist/@pve/qat-invoke.sh
[setup-nfd.md]: setup-nfd.md
[QAT Developers page]: https://www.intel.com/content/www/us/en/developer/topic-technology/open/quick-assist-technology/overview.html
