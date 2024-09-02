# Setup IAA

This page describes Intel® In-Memory Analytics Accelerator (IAA) setup.

## IAA Host Setup

* The SPR D0 above platform is required to run any IAA workload.   
* Linux kernel 5.16 or above needs to be installed in the system. 
* The BIOS must be configured with `VT-d` and `PCI ENQCMD` enabled, as follows:  

    ```
    EDKII Menu → Socket Configuration → IIO Configuration → Intel VT for directed IO (VT-d) → Intel VT for directed IO → Enable
    EDKII Menu → Socket Configuration → IIO Configuration → Intel VT for directed IO (VT-d) Option: No → Yes
    EDKII Menu → Socket Configuration → IIO Configuration → Interrupt Remapping Option: No → Yes
    EDKII Menu → Socket Configuration → IIO Configuration → PCIe ENQCMD/ENQCMDS → Enable
    EDKII Menu → Socket Configuration → Processor Configuration -> VMX -> Enable
    ```

* The BIOS must be configured with `Illegal MSI Mitigation` enabled for SKUs other than SPR E5, as follows:  

    ```
    EDKII Menu → Socket Configuration → IIO Configuration → Intel VT for directed IO (VT-d) → Opt-Out Illegal MSI Mitigation → Enable
    ```

* The `VT-d` must be enabled from the kernel command line.  

    ```
    sudo grubby --update-kernel=DEFAULT --args="intel_iommu=on,sm_on no5lvl"
    sudo reboot
    ```

## Node Labels

Label the IAA worker node(s) with the following label:
- `HAS-SETUP-IAA=yes`

## Using user-space driver

For Intel® IAA devices, they are currently (at time of writing) appearing as devices with type “0cfe”.
* Device self-check
    ```
    sudo su
    lspci | grep 0cfe
    6a:02.0 System peripheral: Intel Corporation Device 0cfe
    6f:02.0 System peripheral: Intel Corporation Device 0cfe
    74:02.0 System peripheral: Intel Corporation Device 0cfe
    79:02.0 System peripheral: Intel Corporation Device 0cfe
    e7:02.0 System peripheral: Intel Corporation Device 0cfe
    ec:02.0 System peripheral: Intel Corporation Device 0cfe
    f1:02.0 System peripheral: Intel Corporation Device 0cfe
    f6:02.0 System peripheral: Intel Corporation Device 0cfe
    ```

## Using kernel-space driver

* Download, build and install the [accel-config][accel-config] driver as follows:
    ```
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
* Configure the IAA devices by using the accel-config utility. e.g  enabling iax1 and wq1.0. The detail configuration file and scripts can be found in https://github.com/intel-innersource/applications.databases.thirdparty.clickhouse-hero/blob/ck2112_iaa_dev/benchmark/iaadeflate/iaa_setup

    ```
    accel-config load-config -c ./accel-iaa-8d1g8e.conf
    accel-config enable-device iax1
    accel-config enable-wq iax1/wq1.0
    accel-config enable-device iax3
    accel-config enable-wq iax3/wq3.0
    accel-config enable-device iax5
    accel-config enable-wq iax5/wq5.0
    accel-config enable-device iax7
    accel-config enable-wq iax7/wq7.0
    accel-config enable-device iax9
    accel-config enable-wq iax9/wq9.0
    accel-config enable-device iax11
    accel-config enable-wq iax11/wq11.0
    accel-config enable-device iax13
    accel-config enable-wq iax13/wq13.0
    accel-config enable-device iax15
    accel-config enable-wq iax15/wq15.0
    ```

* Ensure the `WQ,`s are correctly activated and the devices are registered correctly:

    ```
    cat /sys/bus/dsa/devices/iax1/wq1.0/state
    # enabled
    cat /sys/bus/dsa/devices/iax3/wq3.0/state
    # enabled
    ls /dev/iax/
    # wq1.0  wq11.0  wq13.0  wq15.0  wq3.0  wq5.0  wq7.0  wq9.0
    ```

## See Also

- [IDXD homepage][IDXD homepage]
- [IAA DEFLATE RECIPE][IAA DEFLATE RECIPE]


[accel-config]: https://github.com/intel/idxd-config
[IDXD homepage]: https://intelpedia.intel.com/IDXD
[IAA DEFLATE RECIPE]: https://github.com/intel-innersource/applications.databases.thirdparty.clickhouse-hero/blob/ck2112_iaa_dev/benchmark/iaadeflate