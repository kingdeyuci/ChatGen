# Setup TDX

This document describes how to setup Trust Domain Extensions (TDX). This CPU feature allows Total Memory Encryption (TME) using an external "domain" key, also called a "user" or "tenant" key.

## HW Configuration
* TXT Agent Jumper (S3F1.2) is set to ON on CPU 0
* TXT_PLTEN jumper is set to enable on both the Socket. S3F2.2 and S7E2.2 to OFF

## BIOS Configuration
* EDKII MENU -> Socket Configuration -> Memory Configuration -> Memory Map
    Set Volatile Memory Mode to 1LM

* EDKII MENU -> Socket Configuration -> Processor Configuration -> TME, TME-MT, TDX
    Set Total Memory Encryption (TME) to Enabled
    Set Total Memory Encryption (TME) Bypass to Disable
    Set Total Memory Encryption Multi-Tenant (TME-MT) to Enabled
    Set TME-MT memory integrity to Enabled
    Set Trust Domain Extension (TDX) to Enabled
    Set the TME-MT/TDX key split to non zero value
* EDKII MENU -> Socket Configuration -> Processor Configuration -> Software Guard Extension (SGX) - Set SW Guard Extensions (SGX) to Enabled
* EDKII MENU -> Socket configuration -> Uncore configuration -> Uncore General Configuration -> Directory Mode: Disable
* EDKII MENU -> Platform Configuration -> System Event log -> eMCA settings - Set EMCA CMCI-SMI Morphing to disable
* EDKII MENU -> Socket Configuration -> Processor Configuration -> - Set Disable excluding Mem below 1MB in CMR to Enabled

## Launch TDX guest

* Add the following content into /etc/yum.repos.d/tdx-release-repo.repo.
  ```
  [tdx-release-repo]
  name=tdx-release-repo
  baseurl=https://<USER>:<APIKEY>@ubit-artifactory-or.intel.com/artifactory/linuxcloudstacks-or-local/tdx-stack/
  tdx-2021ww39/tdx-repository/
  gpgcheck=0
  enabled=1
  module_hotfixes=true
  metadata_expire=0
  ```

* Install packages
  ```
  sudo dnf install intel-optimized-pkg-tdvf intel-optimized-pkg-qemu-kvm intel-optimized-pkg-tdx-host-kernel-spr intel-optimized-pkg-tdx-module-spr intel-optimized-pkg-libvirt
  ```

* Reboot system

* Download guest image and kernel image
  * [CentOS8.4 EFI cloud-init TD guest image][CentOS8.4 EFI cloud-init TD guest image]
  * [TD guest kernel image][TD guest kernel image]

* Create host-only network in qemu
  ```shell
  sudo virsh net-define host-only.xml && sudo virsh net-start host-only
  host-only.xml
  <network>
      <name>host-only</name>
      <bridge name='vir-host' />
      <ip address='192.168.200.1' netmask='255.255.255.0'>
          <dhcp>
              <range start='192.168.200.2' end='192.168.200.253'/>
          </dhcp>
      </ip>
  </network>
  ```
* Make sure libvirtd service started
* Create additional filesystem 

  >Before using it, need to install the following dependency packages
  ```shell
  sudo dnf install virt-install wget
  ```

With dependency packages installed, the system is ready for the next steps:
* Extract the image creation tool:
  ```shell
  mkdir cloud-image-tool && cd cloud-image-tool
  tar xvf ../os.linux.cloud.tdx.tdx-cloud-image-tool-2021WW*.tar.gz
  cd os.linux.cloud.tdx.tdx-cloud-image-tool-2021WW*/
  ```

* Change default IMAGE_SIZE value in script create-td-img.sh to 500, 2 locations.
  ```
  36 IMAGE_TARGET="base"
  37 VIRT_VM_NAME="${TDX_BASE_VIRT_VM_NAME}"
  38 IMAGE_NAME="${VIRT_VM_NAME}.qcow2"
  39 IMAGE_SIZE=500    // update value here
  40 VIRT_VM_MEM_SIZE=16384
  41 VIRT_VM_VCPUS=32
  ```
  ```
  89 set_parameters() {
  90     case $IMAGE_TARGET in
  91     base)
  92         VIRT_VM_NAME="${TDX_BASE_VIRT_VM_NAME}"
  93         IMAGE_NAME="${VIRT_VM_NAME}.qcow2"
  94         IMAGE_SIZE=500    // update value here
  ```
* Save the create-td-img.sh file.

* Create base image: td-guest-centos8.4.qcow2
  ```shell
  ./create-td-img.sh -t base
  ```

* Launch TDX guest with virsh
  ```yaml
  virsh create tdx.xml

  tdx.xml
  <domain type='kvm' xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0'>
    <name>tdx-97837</name>
    <memory unit='KiB'>234881024</memory>
    <vcpu placement='static'>32</vcpu>
    <os>
      <type arch='x86_64' machine='pc-q35-3.0'>hvm</type>
      <loader type='generic'>/usr/share/qemu/TDVF.fd</loader>
      <boot dev='hd'/>
      <kernel>/home/raspadmin/vmlinuz</kernel>
      <cmdline>root=/dev/vda3 selinux=0 rw console=hvc0 ignore_loglevel tdx-guest tdx_disable_filter force_tdx_guest</cmdline>
    </os>
    <features>
      <acpi/>
      <apic/>
      <ioapic driver='qemu'/>
      <pic state='off'/>
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
    <cpu mode='host-passthrough'>
      <topology sockets='2' cores='16' threads='1'/>
    </cpu>
    <devices>
      <emulator>/usr/libexec/qemu-kvm</emulator>
      <disk type='file' device='disk'>
        <driver name='qemu' type='qcow2'/>
        <source file='/home/tdx_image_tool/td-guest-centos8.4.qcow2'/>
        <target dev='vda' bus='virtio'/>
      </disk>
      <serial type='pty'>
        <target type='isa-serial' port='0'/>
      </serial>
      <console type='pty'>
        <target type='serial' port='0'/>
      </console>
      <console type='pty'>
        <target type='virtio' port='1'/>
      </console>
      <vsock model='virtio'>
        <cid auto='yes' address='3'/>
        <address type='pci' domain='0x0000' bus='0x05' slot='0x00' function='0x0'/>
      </vsock>
      <interface type="network">
        <source dev='enp1s0' network="host-only"/>
        <mac address="52:54:00:a6:d2:79"/>
        <model type="virtio"/>
      </interface>
    </devices>
    <allowReboot value='no'/>
    <launchSecurity type='tdx'>
      <policy>0x1</policy>
    </launchSecurity>
    <qemu:commandline>
      <qemu:arg value='-cpu'/>
      <qemu:arg value='host,-kvm-steal-time,pmu=off'/>
    </qemu:commandline>
  </domain>
  ```

* Configure SSH tunnel between Host and Guest

On the VM:
```bash
ip route add default via 192.168.200.1 dev enp1s0
cat > /etc/resolv.conf <<EOF
search gv.intel.com
nameserver 10.248.2.1
nameserver 10.22.224.196
nameserver 10.3.86.116
EOF
```
On the host:
```bash
sudo iptables -t nat -F
sudo iptables -t nat -A POSTROUTING -s 192.168.200.0/24 -d 0/0 -j MASQUERADE
sudo iptables -I FORWARD -j ACCEPT -i vir-host
sudo iptables -I FORWARD -j ACCEPT -o vir-host
ssh -f -N -L 0.0.0.0:4022:127.0.0.1:22 root@192.168.200.89
```

* Setup docker and k8s on VM
After setup k8s, need to change k8s hostname to host ip, otherwise no pod will be scheduled.
  ```bash
  kubectl label node td-guest kubernetes.io/hostname=10.219.170.133 --overwrite
  ```

[CentOS8.4 EFI cloud-init TD guest image]: http://cpio-devops-pub.sh.intel.com/download/tdx-guest/tdx-2021ww39/td-guest-centos8.4.qcow2.tar.xz
[TD guest kernel image]: http://cpio-devops-pub.sh.intel.com/download/tdx-guest/tdx-2021ww39/vmlinuz