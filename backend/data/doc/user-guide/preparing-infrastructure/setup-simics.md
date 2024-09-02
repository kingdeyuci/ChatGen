# Setup Simics

Simics is a full-system virtual platform simulation framework. It supports building fast transaction-level models of complete digital systems, from single SoCs to boards to systems to networks of systems.

## Prerequisite

- **AGS Entitlement**: See the list of
  [AGS entitlements][AGS entitlements]
  for details:
  - For SPR, entitlements required:
    - Simics Keys Read
    - Artifactory Simics BB Viewer
    - Simics Eagle Stream access
    - Simics Sapphire Rapids access
    - Simics TS CPU access
    - Simics PnP access
    - Simics Xtensa Models access
  - For GNR, entitlements required:
    - Simics Keys Read
    - Artifactory Simics BB Viewer
    - Simics Granite Rapids access
    - Simics Donahue Valley access
- **Kerberos**: Follow the [instructions][instructions] to install and
  configure Kerberos.
- **NTP**: Install `NTP` or make sure your machine date time is correct.
- Install `smbclient`, `p7zip-full` (Ubuntu) /`samba-client`,
  `p7zip-plugins` (CentOS: from `epel-release`).

## Platforms

You can refer to the following artifactory paths to get the specific Simics packages:

- [SPR][SPR]
- [GNR][GNR]

## Installation

- Download the Simics packages as follows (example for SPR):

    ```shell
    mkdir simics-downloads
    cd simics-downloads
    # replace YearwwXX.y with the latest release versions, e.g. 2022ww44.3
    wget --no-proxy -r -nd -np -A tar https://simics-artifactory.devtools.intel.com/artifactory/list/simics-repos/vp-release/6.0/egs-os/Silver/YearwwXX.Y/
    for p in *tar; do tar xvf $p; done
    ```

    > To check other platforms packages and the most current versions, visit [the Index of simics-repos/][simics-repos].

- Install Simics as follows:

    ```shell
    cd simics-6-install
    ./install-simics.pl
    # when prompt, install simics to your home directory ~/simics
    ```

- Compile VMP kernel module:

  - **Cent OS**: Install `gcc-c++`, `kernel-headers`, `kernel-devel`,
    and `elfutils-devel`.
  - **Ubuntu**: Install `c++`, `linux-headers-$(uname -r)`, and `libelf-dev`.

    ```shell
    cd ~/simics/simics-6/simics-6.0.71
    bin/vmp-kernel-install
    ```

    The VMP module must be reloaded after reboot:

    ```shell
    cd ~/simics/simics-6/simics-6.0.71
    bin/vmp-kernel-load
    ```

## Project Setup

- Create the project workspace:

    ```shell
    cd ~/simics/simics-6/simics-6.0.71
    bin/project-setup ~/simics-eaglestream/
    ```

## Platform Launch

- Launch the Simics platform:

    ```shell
    cd ~/simics-eaglestream/
    ./simics targets/eaglestream/eaglestream.simics -no-win
    ```

    Use these Simics configurations as reference to use a separate disk image, enable network and/or define system resources:
    - [SPR][SPR-sim]
    - [GNR][GNR-sim]

## See Also

- [Simics Wiki][Simics Wiki]
- [Install Kerberos][Install Kerberos]
- [Install Intel certificates][Install Intel certificates]

### SPR

```shell
$artifactory = TRUE
# $disk_image = /home/user/xmg/xtp/images/workloadsvalidation50gb.img

enable-real-time-mode

$rtc_time = "2020-10-01 08:08:08 UTC" # ( date format="%Y-%m-%d %H:%M:%S")
$create_network = TRUE
$real_network = TRUE
if not defined gbe_softstrap_wa { $gbe_softstrap_wa = TRUE } # Work-around for eth HSD1507023291

$bios_knobs_string="VTdSupport=1,PcieEnqCmdSupport=1"
$bios_knobs="vtd_enqcmd" # can be anything

# $dimms_per_socket=8
# $memory_per_dimm=65536

# enable-mca
$uncore_revision=e0

# $num_cpus = 1
# $n_cores = 1
# $n_threads = 1

# $halt_steps = False
# $use_halt_steps = False
# $cpu_halt_steps = False

run-command-file targets/eaglestream/eaglestream.simics

eaglestream.mb.cpu0.core[0][0]->cpuid_monitor_mwait_enabled_override=0

connect-real-network "192.168.1.150"
connect-real-network-port-in ethernet-link = ethernet_switch0 target-ip = 192.168.1.150 target-port = 6443 host-port = 6443 -tcp

# Enable TMUL flags
@cores = [obj for obj in SIM_get_all_objects() if obj.classname == 'x86-glc' ]
@for c in cores : c.cpuid_avx512_bf16_override = 1

if not defined cpuid_disable_avx512 { $cpuid_disable_avx512 = FALSE }
if not defined cpuid_disable_amx    { $cpuid_disable_amx = FALSE }

    # 20ww34 - disable 5-level paging and AVX-512, and additional cpuid tweaks and optimization from Samuel Rydh
    foreach $s in (range $num_cpus) { foreach $c in (range $n_cores) { foreach $t in (range $n_threads) {
        $cpu = $system + ".mb.cpu" + $s + ".core[" + $c + "][" + $t + "]"
        # disable 5 level paging
        $cpu->cpuid_la57_override                 = 0
        $cpu->cpuid_physical_bits_override        = 46
        $cpu->cpuid_linaddr_width_override        = 48

        if $cpuid_disable_avx512 {
            # disable avx512
            $cpu->cpuid_has_avx512f_override          = 0
            $cpu->cpuid_avx512_4fmaps_override        = 0
            $cpu->cpuid_avx512_4vnniw_override        = 0
            $cpu->cpuid_avx512_bf16_override          = 0
            $cpu->cpuid_avx512_bitalg_override        = 0
            $cpu->cpuid_avx512_vbmi2_override         = 0
            $cpu->cpuid_avx512_vpopcntdq_override     = 0
            $cpu->cpuid_avx512bw_override             = 0
            $cpu->cpuid_avx512cd_override             = 0
            $cpu->cpuid_avx512dq_override             = 0
            $cpu->cpuid_avx512er_override             = 0
            $cpu->cpuid_avx512fp16_override           = 0
            $cpu->cpuid_avx512ifma_override           = 0
            $cpu->cpuid_avx512pf_override             = 0
            $cpu->cpuid_avx512vbmi_override           = 0
            $cpu->cpuid_avx512vl_override             = 0
            $cpu->cpuid_avx512vnni_override           = 0
            $cpu->cpuid_avx512vp2intersect_override   = 0
        }
        if $cpuid_disable_amx {
            $cpu->cpuid_amx_bf16_override             = 0
            $cpu->cpuid_amx_int8_override             = 0
            $cpu->cpuid_amx_tile_override             = 0
        }

        $cpu->cpuid_pks_override                  = 0
        $cpu->cpuid_pku_override                  = 0

        $cpu->cpuid_cet_ss_override               = 0
        $cpu->cpuid_cet_ibt_override              = 0

        $cpu->cpuid_bus_lock_intercept_override   = 0 # https://hsdes.intel.com/appstore/article/#/22012461787

        $cpu->cpuid_monitor_mwait_enabled_override = 0 # @cpuid_ovrd_disable_mwait()

    } } }
    script-branch {
        $system.serconsole.con.wait-for-string "Press 'e' to edit the selected item"
        # Remove event bottleneck
        if $system=="eaglestream" {
            foreach $s in (range $num_cpus) {
                ($system + ".mb.nb" + $s + ".lpss[0]")->internal_state_service_interval = 0x10000
                ($system + ".mb.nb" + $s + ".lpss[1]")->internal_state_service_interval = 0x10000
            }
        }
        if $system=="birchstream" {
            foreach $s in (range $num_cpus) { foreach $d in (range $num_c_dies) {
                ($system + ".mb.soc" + $s + ".c_die" + $d + ".spdi3c[0]")->internal_state_service_interval = 0x10000
                ($system + ".mb.soc" + $s + ".c_die" + $d + ".spdi3c[1]")->internal_state_service_interval = 0x10000
            }}
        }
    }
    script-branch {
        $system.serconsole.con.wait-for-string "Press [F2]"
        # 20ww32 - disable EPT Accessed/Dirty feature so we can get speed-up from VMP
        foreach $s in (range $num_cpus) { foreach $c in (range $n_cores) { foreach $t in (range $n_threads) {
            $cpu = $system + ".mb.cpu" + $s + ".core[" + $c + "][" + $t + "]"
            $cpu->ia32_vmx_ept_vpid_cap = $cpu->ia32_vmx_ept_vpid_cap & (~(1<<21))
            #@print("\nDEBUG : disable EPT Accessed/Dirty feature for S%d_C%d_T%d" % (simenv.s,simenv.c,simenv.t))
        } } }
    }
```
### GNR

```shell
# $disk_image = /nfs/site/disks/simcloud_users/aarcemor/workloadsvalidation50gb.img

$rtc_time = "2021-24-04 13:03:08 UTC" # ( date format="%Y-%m-%d %H:%M:%S")
$enable_i82599_real_network=TRUE

$bios_knobs_string="VTdSupport=1,PcieEnqCmdSupport=1"
$bios_knobs="vtd_enqcmd" # can be anything

# $dimms_per_socket=8
# $memory_per_dimm=16384

# $num_cpus = 1
# $n_cores = 1
# $n_threads = 1

run-command-file "/nfs/site/disks/simcloud_users/aarcemor/simics/simics-6.0.105/../simics-graniterapids-6.0.pre414/targets/birchstream/birchstream-sp.simics"

enable-real-time-mode
connect-real-network "10.10.0.100"

connect-real-network-port-in ethernet-link = ethernet_switch0 target-ip = 10.10.0.100 target-port = 6443 host-port = 6443 -tcp
```

[AGS entitlements]: https://wiki.ith.intel.com/pages/viewpage.action?pageId=1059037612#Simics6-SimicsPackages
[instructions]: kerberos.md
[SPR]: https://simics-artifactory.devtools.intel.com/artifactory/list/simics-repos/vp-release/6.0/egs-os/Silver/
[GNR]: https://simics-artifactory.devtools.intel.com/artifactory/list/simics-repos/vp-release/6.0/gnr/Silver/
[SPR-sim]: simics-conf-spr.md
[GNR-sim]: simics-conf-gnr.md
[Simics Wiki]: http://goto.intel.com/simics
[Install Kerberos]: kerberos.md
[Install Intel certificates]: https://github.com/intel-innersource/applications.benchmarking.benchmark.platform-hero-features/wiki/Install-Intel-Certificates
[simics-repos]: https://simics-artifactory.devtools.intel.com/artifactory/list/simics-repos/