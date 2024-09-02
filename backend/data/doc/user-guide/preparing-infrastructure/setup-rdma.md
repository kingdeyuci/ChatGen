# Setup network

For the workload depend on the network RDMA, the test environment must be prepared in advance.

Install the NICs that support RDMA function (including iWARP and RoCE) and link multiple workers together using either a high-speed switch or point-to-point cross-link cables. The network interface can be either a physical interface or a logical bond of multiple physical interfaces.

For example, on each Linux Host, you shall install Intel E810-xxx or Mellanox ConnectX-3/4 NIC adaptor.

## Setup for NIC RDMA driver

- Intel E810-xxx and X722 RDMA NICs
  - Download the NIC driver and decompress the irdma driver archive:
```
    tar zxf irdma-<version>.tgz
```
  - Build and install the RDMA driver:
```
    cd irdma-<version>
    ./build.sh
```

- Mellanox ConnectX-3 RDMA NICs
```
  modprobe mlx4_core
  modprobe mlx4_ib
  modprobe mlx4_en
```
- Mellanox ConnectX-4 RDMA NICs
```
  modprobe mlx5_core
  modprobe mlx5_ib
```

## Setup for RDMA generic driver
Load the RDMA drivers :
  ```
  modprobe ib_cm
  modprobe ib_core
  # Please note that ib_ucm does not exist in newer versions of the kernel and is not required.
  modprobe ib_ucm || true
  modprobe ib_umad
  modprobe ib_uverbs
  modprobe iw_cm
  modprobe rdma_cm
  modprobe rdma_ucm
  ```

## Verify the RDMA functionality
- Run `ibv_devices` command to check RDMA device
    # ibv_devices
    device                 node GUID
    ------              ----------------
    rdmap175s0f0        40a6b70b6f300000
    rdmap175s0f1        40a6b70b6f310000

- Check /sys device node
  Each RDMA device is associated with a network interface. The sysfs filesystem
  can help show how these devices are related. For example:
  - To show RDMA devices associated with the "ens801f0" network interface:
    ```
    # ls /sys/class/net/ens801f0/device/infiniband/
    rdmap175s0f0
    ```
  - To show the network interface associated with the "rdmap175s0f0" RDMA device:
  ```
    # ls /sys/class/infiniband/rdmap175s0f0/device/net/
    ens801f0
  ```

### Node Labels:

Label the worker nodes with the following node labels:
- `HAS-SETUP-RDMA=yes`: Required

## See Also:

- [Intel RDMA NIC Adaptor][Intel RDMA NIC website]

[Intel RDMA NIC website]: https://www.intel.com/content/www/us/en/download/19632/linux-rdma-driver-for-the-e810-and-x722-intel-ethernet-controllers.html
