# FlexRAN Setup
## System Setup

Perform the following system setup for FlexRAN to function properly:

- OS = CentOS-7
- Real time kernel = kernel-rt-3.10.0-1127.19.1.rt56.1116.el7.x86-64.rpm
- BIOS =  S2600WF_EFI-BIOSR0013_ME04.00.04.294

- Following Bios Settings are needed for FlexRan to function:

    ```
    Advanced -> Power & Performance -> CPU Power and Performance Policy -> Performance
    Advanced -> Power & Performance -> Uncore Power Management -> Enabled
    Advanced -> Power & Performance -> Hardware P States -> Disabled
    Advanced -> Power &Performance -> CPU C State Control -> C0/C1 state
    Advanced -> Power & Performance -> Memory Configuration -> Memory RAS and performance Configuration -> NUMA Optimized -> Enabled
    Advanced -> Processor Configuration -> Intel(R) Hyper-Threading Tech -> Disabled
    Advanced -> Processor Configuration -> LLC Prefetch -> Enabled
    Advanced -> Advanced Boot Options -> Boot Mode -> Legacy
    Advanced -> Power -> CPU P State Control -> Enhanced Intel SpeedStep(R) Tech  -> Enabled
    ```

- Add the proxies to the file /etc/yum.conf

    ```
    proxy=https://[Enter the proxy information here]
    http_proxy=http://[Enter the proxy information here]
    ```

- Similarly, if wget also requires proxy setting, then the following lines must be added to wgetrc in /etc. (You may need to create wgetrc if it is not present.)

    ```
    proxy= http://[Enter the proxy information here]
    http_proxy= http://[Enter the proxy information here]
    ```

- Configure Real-Time Repository

    ```
    wget http://linuxsoft.cern.ch/cern/centos/7/rt/CentOS-RT.repo -P /etc/yum.repos.d/
    ```

- Install Real-Time Kernel and Packages

    ```
    yum groupinstall "Development Tools"
    yum remove tuned.noarch -y
    yum install tuned-2.11.0-5.el7fdp.1.noarch.rpm -y
    yum install kernel-rt-3.10.0-1160.11.1.rt56.1145.el7.x86_64 -y
    yum install kernel-rt-devel-3.10.0-1160.11.1.rt56.1145.el7.x86_64 -y

    yum install rtctl-1.13-2.el7.noarch -y
    yum install rt-setup-2.0-9.el7.x86_64 -y
    yum install rt-tests-1.0-16.el7.x86_64 -y
    yum install libcgroup-0.41-21.el7.x86_64 -y
    yum install https://cbs.centos.org/kojifiles/packages/qemu-kvm-ev/2.9.0/16.el7_4.14.1/x86_64/qemu-kvm-tools-ev-2.9.0-16.el7_4.14.1.x86_64.rpm -y
    yum install tuna-0.13-9.el7.noarch -y
    yum install tuned-profiles-nfv-guest-2.11.0-5.el7fdp.1.noarch.rpm -y
    yum install tuned-profiles-nfv-host-2.11.0-5.el7fdp.1.noarch.rpm -y
    yum install libhugetlbfs-devel-2.16-13.el7.i686.rpm -y
    yum install libhugetlbfs-2.16-13.el7.x86_64 -y
    yum install libhugetlbfs-devel-2.16-13.el7.x86_64 -y
    yum install libhugetlbfs-utils-2.16-13.el7.x86_64 -y
    yum install libstdc++-4.8.5-44.el7.x86_64 -y
    yum install libstdc++-devel-4.8.5-44.el7.x86_64 -y
    yum install numactl-devel-2.0.12-5.el7.x86_64 -y
    yum install numactl-2.0.12-5.el7.x86_64 -y
    yum install gcc-c++-4.8.5-44.el7.x86_64 -y
    yum install python3-pip -y
    pip3 install meson
    pip3 install ninja
    git clone https://github.com/pkgconf/pkgconf.git
    cd pkgconf
    ./autogen.sh
    ./configure
    make
    make install
    ```
- Isolate the cores for Real-Time Tasks:

    ```
    lscpu|grep NUMA
    NUMA node(s): 2
    NUMA node0 CPU(s): 0-19
    NUMA node1 CPU(s): 20-39
    ```
- Edit /etc/tuned/realtime-virtual-host-variables.conf to add isolated_cores=1-39:
 
    ```
    isolated_cores=1-19， 21-39
    ```

- To activate Real-Time Profile, run command:

    ```
    tuned-adm profile realtime-virtual-host
    ```

- Then check the Wolf Pass server:

    ```
    grep tuned_params= /boot/grub2/grub.cfg
    set tuned_params="isolcpus=1-39 intel_pstate=disable nosoftlockup skew_tick=1 nohz=on nohz_full=1-19， 21-39 rcu_nocbs=1-19， 21-39"
    ```


- Edit /etc/default/grub and append the following to the GRUB_CMDLINE_LINUX:

    ```
    “processor.max_cstate=1 intel_idle.max_cstate=0 intel_pstate=disable idle=poll default_hugepagesz=1G hugepagesz=1G hugepages=50 intel_iommu=on iommu=pt selinux=0 enforcing=0 nmi_watchdog=0 audit=0 mce=off kthread_cpus=0 irqaffinity=0 idle=poll”
    GRUB_CMDLINE_LINUX_DEFAULT="${GRUB_CMDLINE_LINUX_DEFAULT:+$GRUB_CMDLINE_LINUX_DEFAULT}\$tuned_params" GRUB_INITRD_OVERLAY="${GRUB_INITRD_OVERLAY:+$GRUB_INITRD_OVERLAY }\$tuned_initrd"
    ```

- For example

    ```
    GRUB_TIMEOUT=5
    GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
    GRUB_DEFAULT=saved
    GRUB_DISABLE_SUBMENU=true
    GRUB_TERMINAL_OUTPUT="console"
    GRUB_CMDLINE_LINUX="crashkernel=auto rhgb quiet"
    GRUB_DISABLE_RECOVERY="true"
    GRUB_CMDLINE_LINUX_DEFAULT="${GRUB_CMDLINE_LINUX_DEFAULT:+$GRUB_CMDLINE_LINUX_DEFAULT
    }\$tuned_params"
    GRUB_INITRD_OVERLAY="${GRUB_INITRD_OVERLAY:+$GRUB_INITRD_OVERLAY }\$tuned_initrd"
    GRUB_CMDLINE_LINUX=" crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb
    quiet processor.max_cstate=1 intel_idle.max_cstate=0 intel_pstate=disable idle=poll
    default_hugepagesz=1G hugepagesz=1G hugepages=64 intel_iommu=on selinux=0 enforcing=0
    nmi_watchdog=0 audit=0 mce=off kthread_cpus=0 irqaffinity=0 console=tty0
    console=ttyS0,115200n8”
    ```

- After the change, the grub file runs the following command to update the grub:

    ```
    grub2-mkconfig -o /boot/grub2/grub.cfg
    ```

- Reboot the server, and check the kernel parameter, which should look like:

    ```
    cat /proc/cmdline
    BOOT_IMAGE=/vmlinuz-3.10.0-1062.12.1.rt56.1042.el7.x86_64 root=UUID=9b3e69f6-88af-4af1-
    8964-238879b4f282 ro crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb
    quiet processor.max_cstate=1 intel_idle.max_cstate=0 intel_pstate=disable idle=poll
    default_hugepagesz=1G hugepagesz=1G hugepages=64 intel_iommu=on selinux=0 enforcing=0
    nmi_watchdog=0 audit=0 mce=off kthread_cpus=0 irqaffinity=0 console=tty0 console=ttyS0,115200n8 skew_tick=1 isolcpus=1-39 intel_pstate=disable nosoftlockup
    nohz=on nohz_full=1-39 rcu_nocbs=1-39
    ```

- Set CPU frequency using msr-tools:

    ```
    git clone https://github.com/intel/msr-tools/
    cd msr-tools/
    git checkout msr-tools-1.3
    make
    cat <<EOF > turbo-2.2G.sh
    #!/bin/sh
    for i in {0..39}
    do
    #Set core 0-39 to 2.2GHz (0x1600). Please change according to your CPU model
    ./wrmsr -p \${i} 0x199 0x1600
    done
    #Set Uncore to Max
    ./wrmsr -p 0 0x620 0x1e1e
    ./wrmsr -p 39 0x620 0x1e1e
    EOF
    chmod 755 turbo-2.2G.sh
    sh turbo-2.2G.sh
    ```

## Install Docker
For installation and setup refer to [docker setup][docker setup]

Additional requirements for FlexRAN workload:

- Install additional packages

    ```
    yum install -y device-mapper-persistent-data lvm2
    ```

- Install docker version *19.03.12*

- Setup docker daemon
    ```
    mkdir /etc/docker
    cat > /etc/docker/daemon.json <<EOF
    {
    "exec-opts": ["native.cgroupdriver=systemd"],
    "log-driver": "json-file",
    "log-opts": {
    "max-size": "100m"
    },
    "storage-driver": "overlay2",
    "storage-opts": [
    "overlay2.override_kernel_check=true"
    ]
    }
    EOF
    ```

- [Proxy setup][Proxy setup]. Append *\<HOST-IP\>* to *noProxy*.

- FlexRAN repos are cloned and build in docker image. This requires large disk space. If the default disk */var/lib/docker* is not having enough disk space, then specify a partition (*E.g "data-root": "/home/docker"*) with large space in 'daemon.json'. Reload and restart docker daemon.


## Install Kubernetes
For installation and setup refer to [kubernetes setup][kubernetes setup].

Additional requirements for FlexRAN workload:

- Install kubernetes version *1.18.6*

    ```
    yum install -y kubelet-1.18.6 kubeadm-1.18.6 kubectl-1.18.6 --disableexcludes=kubernetes
    ```

- Append *\<HOST IP\>* to *no_proxy*

- Initialise cluster with version *1.18.6*

    ```
    kubeadm init --kubernetes-version=v1.18.6 --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=<master-node-ip> --token-ttl 0
    ```

- Kubeadm init may fail because of kubelet service. Restart kubelet service, since the above init command has created required config files and keys. Then re-run kubeadm init by ignoring preflight errors.

    ```
    systemctl daemon-reload
    systemctl restart docker
    systemctl restart kubelet
    kubeadm init --kubernetes-version=v1.18.6 --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address=<master-node-ip> --token-ttl 0 --ignore-preflight-errors all
    ```

- Instead of *flannel* install *Multus* and *Calico*

    ```
    git clone https://github.com/intel/multus-cni
    cd /root/multus-cni/images
    git checkout v3.3
    kubectl create -f multus-daemonset.yml
    kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml
    ```
## SRIO network plug-in

git clone https://github.com/k8snetworkplumbingwg/sriov-network-device-plugin

cd /sriov-network-device-plugin/deployments/

# Check & Edit resourceName and devices in configMap.yaml file in /sriov-network-device-plugin/deployments/

#"resourceName": "intel_acc100 & "devices": ["0d5c"]

kubectl create -f deployments/configMap.yaml

kubectl create -f deployments/k8s-v1.16/sriovdp-daemonset.yaml

# Use the pf-bb-config application from GitHub to configure FPGA resources for different VFs

#let example FEC pcie bus is 0000:18:00.0 

```

git clone http://dpdk.org/git/dpdk-kmods

cd dpdk-kmods/linux/igb_uio

make

export RTE_SDK_KMOD=$localPath/dpdk-kmods

modprobe uio

insmod $RTE_SDK_KMOD/linux/igb_uio/igb_uio.ko

./dpdk-devbind.py -s  # To check status  #(/wireless_dpdk_ae/usertools)

./dpdk-devbind.py -b igb_uio 0000:18:00.0 #To bind the Fec device

#build inih

git clone  https://github.com/benhoyt/inih  (to /home/5gnr_platform/ directory)

cd inih

git checkout r44

cd extra

make -f Makefile.static

cp libinih.a ../

#build pf-bb-config

git clone https://github.com/intel/pf-bb-config.git

(to /home/5gnr_platform/ directory)

export INIH_PATH=/home/5gnr_platform/inih

cd  pf-bb-config

make clean

make

./pf_bb_config ACC100 -c ./acc100/acc100_config_pf.cfg 

```

## Node Labels
Label the FlexRan worker node(s) with the following node labels:
- `HAS-SETUP-KERNEL-RT-3-10=yes`: Must have.
- `HAS-SETUP-CENTOS7=yes`: Must have.
- `HAS-SETUP-ACC100=yes`: Must have.
- `HAS-SETUP-HUGEPAGES-1048576kB-64=yes` Must have.

[docker setup]: setup-docker.md
[Proxy setup]: https://docs.docker.com/network/proxy/#configure-the-docker-client
[kubernetes setup]: setup-kubernetes.md