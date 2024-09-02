# Setup KVM

This document is specific for SPR-VM with AMX enabled.

## Prerequisites
Below configuration is verified ONLY on `Centos Stream 8` (Reference: PAIV DL Boost Package Release).

Here are suggestions for Ubuntu OS:

- Ubuntu 22.04 should have no support of AMX with build-in kernel. Please update kernel to V5.17+ and V7.0+ respectively, and create VM by using qemu-system-x86_64 directly.
- Ubuntu 22.10 has full support of Intel AMX (https://linux-ftp.intel.com/pub/mirrors/ubuntu-releases/22.10/). You can create an VM by using virt-install.

## Enable AMX Feature in Qemu
* Pre-Request
    * Enter into the container and download the pre-request packages
      ```shell
      sudo yum install -y git glib2-devel libfdt-devel pixman-devel zlib-devel bzip2 ninja-build python3 libaio-devel libcap-devel libiscsi-devel numactl-devel
      sudo yum install make gcc gcc-c++ meson.noarch -y
      ```
* Download source code package and decompress
    ```shell
    wget -c  https://emb-pub.ostc.intel.com/overlay/spr-bkc-pc/3.21-0.1/cs8-spr/repo/src/qemu-6.1.50-10.spr_bkc_pc_1.6.el8.src.rpm
    rpm2cpio qemu-6.1.50-10.spr_bkc_pc_1.6.el8.src.rpm | cpio -idmv
    tar zxvf qemu.tar.gz
    ```
* Compile and Install
    * Configure the qemu for x86_64
    * mkdir build && cd build
      ```shell
      ../configure --enable-kvm --enable-numa --target-list="x86_64-softmmu"  --prefix=/usr/local/qemu
      ```
    * make 
    * make install
* Check Qemu support AMX
  ```shell
  qemu-system-x86_64 --cpu help | grep -i amx
  ```
* Replace the old qemu_kvm binary with the new one
  ```shell
  ln -s /usr/local/qemu/bin/qemu-system-x86_64   /usr/libexec/qemu-kvm
  ```

## Launch KVM Guest
* Download KVM guest image guest.qcow2(guest image provided from PAIV team)
* Install KVM virtualization tools
  ```shell
  sudo dnf -y install bridge-utils virt-top libvirt-devel libguestfs-tools
  ```
* Make sure libvirtd service started
* Create host only network in host
  ```shell
  sudo virsh net-define host-only.xml && sudo virsh net-start host-only
  ```

  `host-only.xml`:
  ```xml
  <network>
      <name>host-only</name>
      <bridge name='vir-host' />
      <ip address='192.168.123.1' netmask='255.255.255.0'>
          <dhcp>
              <range start='192.168.123.2' end='192.168.123.253'/>
          </dhcp>
      </ip>
  </network>
  ```
* Check host-only network started
  ```shell
  virsh net-list --all
  ```
* Launch KVM guest with virsh
  ```shell
  virsh define guest.xml
  ```

  `guest.xml`:
  ```xml
  <domain type='kvm' xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0'>
    <name>centos-8</name>
    <memory unit='GB'>1024</memory>
    <vcpu placement='static'>112</vcpu>
    <cputune>
      <vcpupin vcpu="0" cpuset="0"/>
      <vcpupin vcpu="1" cpuset="1"/>
      <vcpupin vcpu="2" cpuset="2"/>
      <vcpupin vcpu="3" cpuset="3"/>
      <vcpupin vcpu="4" cpuset="4"/>
      <vcpupin vcpu="5" cpuset="5"/>
      <vcpupin vcpu="6" cpuset="6"/>
      <vcpupin vcpu="7" cpuset="7"/>
      <vcpupin vcpu="8" cpuset="8"/>
      <vcpupin vcpu="9" cpuset="9"/>
      <vcpupin vcpu="10" cpuset="10"/>
      <vcpupin vcpu="11" cpuset="11"/>
      <vcpupin vcpu="12" cpuset="12"/>
      <vcpupin vcpu="13" cpuset="13"/>
      <vcpupin vcpu="14" cpuset="14"/>
      <vcpupin vcpu="15" cpuset="15"/>
      <vcpupin vcpu="16" cpuset="16"/>
      <vcpupin vcpu="17" cpuset="17"/>
      <vcpupin vcpu="18" cpuset="18"/>
      <vcpupin vcpu="19" cpuset="19"/>
      <vcpupin vcpu="20" cpuset="20"/>
      <vcpupin vcpu="21" cpuset="21"/>
      <vcpupin vcpu="22" cpuset="22"/>
      <vcpupin vcpu="23" cpuset="23"/>
      <vcpupin vcpu="24" cpuset="24"/>
      <vcpupin vcpu="25" cpuset="25"/>
      <vcpupin vcpu="26" cpuset="26"/>
      <vcpupin vcpu="27" cpuset="27"/>
      <vcpupin vcpu="28" cpuset="28"/>
      <vcpupin vcpu="29" cpuset="29"/>
      <vcpupin vcpu="30" cpuset="30"/>
      <vcpupin vcpu="31" cpuset="31"/>
      <vcpupin vcpu="32" cpuset="32"/>
      <vcpupin vcpu="33" cpuset="33"/>
      <vcpupin vcpu="34" cpuset="34"/>
      <vcpupin vcpu="35" cpuset="35"/>
      <vcpupin vcpu="36" cpuset="36"/>
      <vcpupin vcpu="37" cpuset="37"/>
      <vcpupin vcpu="38" cpuset="38"/>
      <vcpupin vcpu="39" cpuset="39"/>
      <vcpupin vcpu="40" cpuset="40"/>
      <vcpupin vcpu="41" cpuset="41"/>
      <vcpupin vcpu="42" cpuset="42"/>
      <vcpupin vcpu="43" cpuset="43"/>
      <vcpupin vcpu="44" cpuset="44"/>
      <vcpupin vcpu="45" cpuset="45"/>
      <vcpupin vcpu="46" cpuset="46"/>
      <vcpupin vcpu="47" cpuset="47"/>
      <vcpupin vcpu="48" cpuset="48"/>
      <vcpupin vcpu="49" cpuset="49"/>
      <vcpupin vcpu="50" cpuset="50"/>
      <vcpupin vcpu="51" cpuset="51"/>
      <vcpupin vcpu="52" cpuset="52"/>
      <vcpupin vcpu="53" cpuset="53"/>
      <vcpupin vcpu="54" cpuset="54"/>
      <vcpupin vcpu="55" cpuset="55"/>
      <vcpupin vcpu="56" cpuset="56"/>
      <vcpupin vcpu="57" cpuset="57"/>
      <vcpupin vcpu="58" cpuset="58"/>
      <vcpupin vcpu="59" cpuset="59"/>
      <vcpupin vcpu="60" cpuset="60"/>
      <vcpupin vcpu="61" cpuset="61"/>
      <vcpupin vcpu="62" cpuset="62"/>
      <vcpupin vcpu="63" cpuset="63"/>
      <vcpupin vcpu="64" cpuset="64"/>
      <vcpupin vcpu="65" cpuset="65"/>
      <vcpupin vcpu="66" cpuset="66"/>
      <vcpupin vcpu="67" cpuset="67"/>
      <vcpupin vcpu="68" cpuset="68"/>
      <vcpupin vcpu="69" cpuset="69"/>
      <vcpupin vcpu="70" cpuset="70"/>
      <vcpupin vcpu="71" cpuset="71"/>
      <vcpupin vcpu="72" cpuset="72"/>
      <vcpupin vcpu="73" cpuset="73"/>
      <vcpupin vcpu="74" cpuset="74"/>
      <vcpupin vcpu="75" cpuset="75"/>
      <vcpupin vcpu="76" cpuset="76"/>
      <vcpupin vcpu="77" cpuset="77"/>
      <vcpupin vcpu="78" cpuset="78"/>
      <vcpupin vcpu="79" cpuset="79"/>
      <vcpupin vcpu="80" cpuset="80"/>
      <vcpupin vcpu="81" cpuset="81"/>
      <vcpupin vcpu="82" cpuset="82"/>
      <vcpupin vcpu="83" cpuset="83"/>
      <vcpupin vcpu="84" cpuset="84"/>
      <vcpupin vcpu="85" cpuset="85"/>
      <vcpupin vcpu="86" cpuset="86"/>
      <vcpupin vcpu="87" cpuset="87"/>
      <vcpupin vcpu="88" cpuset="88"/>
      <vcpupin vcpu="89" cpuset="89"/>
      <vcpupin vcpu="90" cpuset="90"/>
      <vcpupin vcpu="91" cpuset="91"/>
      <vcpupin vcpu="92" cpuset="92"/>
      <vcpupin vcpu="93" cpuset="93"/>
      <vcpupin vcpu="94" cpuset="94"/>
      <vcpupin vcpu="95" cpuset="95"/>
      <vcpupin vcpu="96" cpuset="96"/>
      <vcpupin vcpu="97" cpuset="97"/>
      <vcpupin vcpu="98" cpuset="98"/>
      <vcpupin vcpu="99" cpuset="99"/>
      <vcpupin vcpu="100" cpuset="100"/>
      <vcpupin vcpu="101" cpuset="101"/>
      <vcpupin vcpu="102" cpuset="102"/>
      <vcpupin vcpu="103" cpuset="103"/>
      <vcpupin vcpu="104" cpuset="104"/>
      <vcpupin vcpu="105" cpuset="105"/>
      <vcpupin vcpu="106" cpuset="106"/>
      <vcpupin vcpu="107" cpuset="107"/>
      <vcpupin vcpu="108" cpuset="108"/>
      <vcpupin vcpu="109" cpuset="109"/>
      <vcpupin vcpu="110" cpuset="110"/>
      <vcpupin vcpu="111" cpuset="111"/>
    </cputune>
    <numatune>
      <memory mode='strict' nodeset='0-1'/>
      <memnode cellid='0' mode='strict' nodeset='0'/>
      <memnode cellid='1' mode='strict' nodeset='1'/>
    </numatune>
    <cpu mode='host-passthrough'>
      <topology sockets='2' cores='56' threads='1'/>
      <numa>
        <cell id="0" cpus="0-55" memory="512" unit="GiB"/>
        <cell id="1" cpus="56-111" memory="512" unit="GiB"/>
      </numa>
    </cpu>
    <os>
      <type arch='x86_64' machine='pc'>hvm</type>
      <boot dev='hd'/>
    </os>
    <features>
      <acpi/>
      <apic/>
      <ioapic driver='qemu'/>
    </features>
    <clock offset='utc'>
      <timer name='hpet' present='no'/>
    </clock>
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>destroy</on_crash>
    <pm>
      <suspend-to-mem enable='no'/>
      <suspend-to-disk enable='no'/>
    </pm>
    <devices>
      <emulator>/usr/bin/qemu-system-x86_64</emulator>
      <disk type='file' device='disk'>
        <driver name='qemu' type='qcow2'/>
        <source file='/home/vms/guest.qcow2'/>
        <target dev='vda' bus='virtio'/>
      </disk>
      <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0'/>
      <interface type='network'>
        <mac address='52:54:00:cd:48:11'/>
        <source network='host-only'/>
        <model type='virtio'/>
      </interface>
      <serial type='pty'>
        <target type='isa-serial' port='0'/>
      </serial>
      <console type='pty'>
        <target type='virtio' port='1'/>
      </console>
      <vsock model='virtio'>
        <cid auto='yes' address='3'/>
      </vsock>
    </devices>
    <allowReboot value='no'/>
    <qemu:commandline>
      <qemu:arg value='-cpu'/>
      <qemu:arg value='host'/>
    </qemu:commandline>
  </domain>
  ```
* Configure SSH port forwarding

  * Login to the VM using `ssh root@192.168.123.234` with `password:password` and execute a following command:
    ```shell
    ip route add default via 192.168.123.1 dev ens3

    add nameservers in /etc/resolv.conf
    search gv.intel.com
    nameserver 10.248.2.1
    nameserver 10.22.224.196
    nameserver 10.3.86.116
    ```

  * On host:
    ```shell
    sudo iptables -t nat -F
    sudo iptables -t nat -A POSTROUTING -s 192.168.123.0/24 -d 0/0 -j MASQUERADE
    sudo iptables -I FORWARD -j ACCEPT -i vir-host
    sudo iptables -I FORWARD -j ACCEPT -o vir-host
    ssh -f -N -L 0.0.0.0:4022:127.0.0.1:22 root@192.168.123.234
    ```

## Upgrade guest OS kernel

> **Note:** Guest's kernel version should be the same as installed on Host.

* Download kernel package from BKC release
  * [BMC release Kernel][BMC release Kernel]
* Upgrade kernel
  ```shell
  sudo yum localinstall kernel* --skip-broken
  sudo grubby --default-kernel
  sudo grubby --set-default="/boot/vmlinuz-xxxxx"
  ```
* Check system started with upgraded kernel
  ```shell
  uname -a
  ```

## Setup docker and k8s on VM
After setup k8s, need to change k8s hostname to host ip, otherwise no pod will be scheduled.

```shell
kubectl label node kvm-guest kubernetes.io/hostname=10.219.170.133 --overwrite
```

[BMC release Kernel]: https://ubit-artifactory-or.intel.com/artifactory/linuxbkc-or-local/linux-stack-bkc/