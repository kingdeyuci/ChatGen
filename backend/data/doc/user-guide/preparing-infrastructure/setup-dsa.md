# DSA Host Setup

* The SPR platform is required to run any DSA workload.   
* DSA-SPDK-Accel-Perf is known to crash the system on kernel `5.12.0-intel-next.sprd0po.05212021`, while it has been confirmed to work on kernel `5.12.0-0507.intel_next.08_16.2_po.36.x86_64+server`.
* The BIOS must be configured with `VT-d` and `PCI ENQCMD` enabled, as follows:  

    ```
    EDKII Menu → Socket Configuration → IIO Configuration → Intel VT for directed IO (VT-d) → Intel VT for directed IO → Enable
    EDKII Menu → Socket Configuration → IIO Configuration → PCI ENQCMD/ENQCMDS → Yes
    ```

* The `VT-d` must be enabled from the kernel command line.  

    ```shell
    sudo grubby --update-kernel=DEFAULT --args="intel_iommu=on,sm_on iommu=pt"
    sudo reboot
    cat /proc/cmdline
    # BOOT_IMAGE=(hd1,gpt2)/vmlinuz-5.11.0-0224.intel_next.2.x86_64+client root=UUID=48bd5c53-14be-483c-a93d-4f43fc94d719ro rhgb console=tty0 console=ttyS0,115200n8 earlyprintk=ttyS0,115200n8 intel_iommu=on,sm_on
    ```

* Set Kubernetes hugepages:

    ```shell
    sudo grubby --update-kernel=DEFAULT --args "hugepages=512"
    sudo reboot
    kubectl describe node | grep -iA6 capacity
    ```

## Node Labels

Label the DSA worker node(s) with the following label:
- `HAS-SETUP-DSA=yes`
- `HAS-SETUP-HUGEPAGE-2048kB-512=yes`
- `HAS-SETUP-MODULE-VFIO-PCI=yes`

If node is marked with ```HAS-SETUP-MODULE-VFIO-PCI```, make sure the ```vfio-pci``` module is loaded, using ```modprobe vfio-pci``` can insert ```vfio-pci``` module, also using  ```modinfo vfio-pci``` get more about this module info.

## Using user-space driver
For Intel® DSA devices, they are currently (at time of writing) appearing as devices with type “0b25”, This device is binded to vfio_pci and used by spdk.
* Download the SPDK source code
    ```shell
    SPDK_VER=v22.01
    https://github.com/spdk/spdk
    git clone -b ${SPDK_VER} ${SPDK_REPO}
    cd spdk
    git submodule update --init
    ```
* Using the ```dpdk-devbind.py``` script in the SPDK source code.
    ```shell
    sudo su
    lspci | grep 0b25
    6a:01.0 System peripheral: Intel Corporation Device 0b25
    6f:01.0 System peripheral: Intel Corporation Device 0b25
    74:01.0 System peripheral: Intel Corporation Device 0b25
    79:01.0 System peripheral: Intel Corporation Device 0b25
    e7:01.0 System peripheral: Intel Corporation Device 0b25
    ec:01.0 System peripheral: Intel Corporation Device 0b25
    f1:01.0 System peripheral: Intel Corporation Device 0b25
    f6:01.0 System peripheral: Intel Corporation Device 0b25
    cd spdk/
    ./dpdk/usertools/dpdk-devbind.py -u 6a:01.0
    ./dpdk/usertools/dpdk-devbind.py -b vfio-pci 6a:01.0
    ```

* Using the ```setup.sh``` script in the SPDK source code.
    ```shell
    sudo su
    cd spdk/
    PCI_ALLOWED="0000:6a:01.0" ./scripts/setup.sh
    ```
## Using kernel-space driver
These steps aren't required for SPDK-Accel-Perf, but some kernel-based workloads in future may require them.
* Download, build and install the [accel-config][accel-config] driver as follows:
    ```shell
    yum groupinstall "Development Tools"
    yum install autoconf automake libtool pkgconf rpm-build rpmdevtools
    yum install asciidoc xmlto libuuid-devel json-c-devel
    yum install kernel-headers

    git clone -b accel-config-v3.4.5 https://github.com/intel/idxd-config
    cd idxd-config
    ./autogen.sh
    ./configure CFLAGS='-g -O2' --prefix=/usr --sysconfdir=/etc --libdir=/usr/lib64
    make
    make check
    sudo make install
    ```
* Configure the DSA devices by using the accel-config utility. e.g  enabling wq0 and dsa0

    ```
    accel-config disable-wq dsa0/wq0.1
    accel-config disable-device dsa0
    accel-config config-wq --group-id=0 --mode=dedicated --wq-size=128 --type=user --name="dmaengine" --priority=10 --block-on-fault=1 dsa0/wq0.1
    accel-config config-engine dsa0/engine0.0 --group-id=0
    accel-config config-engine dsa0/engine0.1 --group-id=0
    accel-config config-engine dsa0/engine0.2 --group-id=0
    accel-config config-engine dsa0/engine0.3 --group-id=0
    accel-config enable-device dsa0
    accel-config enable-wq dsa0/wq0.1
    ```

* Ensure the `WQ,`s are correctly activated and the devices are registered correctly:

    ```shell
    cat /sys/bus/dsa/devices/dsa0/wq0.0/state
    # enabled
    cat /sys/bus/dsa/devices/dsa0/wq0.1/state
    # enabled
    ls /dev/dsa/
    # wq0.0-0  wq0.1-1
    ```

## See Also

- [Hugepage Setup][Hugepage Setup]
- [IDXD homepage][IDXD homepage]


[accel-config]: https://github.com/intel/idxd-config
[Hugepage Setup]: setup-hugepage.md
[IDXD homepage]: https://intelpedia.intel.com/IDXD