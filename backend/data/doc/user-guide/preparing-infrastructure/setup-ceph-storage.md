# Ceph Storage Setup

This document is a guide for setting up the HW & SW config for build up the rook-ceph cluster for benchmark.

## System Prerequisites:
system prerequisites for building ceph cluster
- Label all the worker node follow section:
  [Node Labels][Node Labels]
- If user run workload on Single Node Kubernetes cluster.
  - Need to remove the taints on the single node cluster for schedulable.     
    `kubectl taint nodes --all node-role.kubernetes.io/master-`
- Kubernetes cluster SW version > 1.21.0 .
- Pre-load rbd driver from linux before the workload running, run `modprobe rbd` to load rbd driver on the node(s), you may need to use `sudo` before to get administration permission.
- Need at least 3 raw drives (Not include the OS drive) on each node for ceph storage cluster building. Use `lsblk` to  make sure there are at least 3 raw drivers.   
- Each raw drive needs the capacity not less 5GiB, and please don't create any filesystem in drives (no partitions or formatted filesystems).
  - Please refer to following section: [drive-clean-up-tool][drive-clean-up-tool]
- Need to install lvm2 utility in the cluster node(s), checking by `sudo lvdisplay`. Use `sudo yum install lvm2` to install lvm2 if you don't have lvm2 currently. 
- python 3 at latest.
- Systemd is needed, generally the popular Linux distributions support it by default.
- Please sync the time according the Timezone(e.g.NTP time sync), this is extremely essential in multi-nodes situation.
  - Please refer to following section: [Time sync][Time sync]
- Make sure docker is installed in each nodes, checking by `docker --version`.
- Please make sure rook-ceph CRDs are deployed before run the test.  
  In the workload/CEPH directory:
  ```shell
    m4 -I../../template template/crds.yaml.m4 > crds.yaml
    kubectl create -f crds.yaml # copy to master node and run
  ```


## Drive Clean up.
If the drives in the system was used before, and was formatted with certain filesystem, please refer to below steps to clean up drive.  
- Check drive name in the node(s)
  ```shell
    lsblk  # first column of the output is the device name.
  ```
- Run [drive_cleanup_script][drive_cleanup_script] in the node(s), please refer to [ceph_drive_clean_examp][ceph_drive_clean_examp]

## Node Labels:

Label the worker nodes with the following node labels: 
- `HAS-SETUP-CEPH-STORAGE=yes`

## Time sync:
Chrony is recommended to sync time in cluster. Chrony may be installed by default. Still if the package is missing, you can easily install it by `yum install -y chrony`. Sync time by
  - `vim /etc/chrony.conf` and change settings
  - start chronyd `systemctl start chronyd`
  - enable chronyd `systemctl enable chronyd` 
## See Also
- [rook-quick-start][rook-quick-start]
- [rook-ceph-prerequisites][rook-ceph-prerequisites]
- [ceph setup HW recommendation][ceph setup HW recommendation]

[Node Labels]: #Node-Labels
[drive-clean-up-tool]: #drive-clean-up
[Time sync]: #Time-sync
[drive_cleanup_script]: ../../script/storage/ceph_cluster_teardown.sh
[rook-quick-start]: https://rook.io/docs/rook/v1.8/quickstart.html
[rook-ceph-prerequisites]: https://rook.io/docs/rook/v1.8/quickstart.html#prerequisites
[ceph setup HW recommendation]: https://docs.ceph.com/en/pacific/start/hardware-recommendations/