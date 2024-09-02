# High Bandwidth Memory (HBM) Setup
This document is a guide for setup Sapphire Rapids (SPR) Xeon Scalable processor with high-bandwidth memory (HBM) environment for WL running. its target is high-bandwidth apps in HPC and AI.

## Specification for SPR HBM
- Four HBM2e stacks
- 64 GB of total HBM capacity per socket
- 8 channels of DDR5

## SPR HBM modes introduction
* 3 Memory Modes deciding how HBM is exposed to software:
  * *HBM-only* : Default mode when no DRAM is present
  * *Flat (1LM)* 
  * *Cache (2LM)* 

* 2 Clustering Modes deciding how the CPU is partitioned:
  * *Quad*: 1 unified NUMA node per socket
  * *SNC4*: Partitions a socket into 4 partitions (NUMA nodes); Provides higher BW and lower latency for accesses within a partition; Needs NUMA aware software (e.g., MPI)

So, we have  6 (3 memory modes X 2 Clustering modes) configurations totally

## SPR HBM Memory mode configuration

### *HBM-only* Mode configuration
* You can remove all DRAM in machine directly , then the default configuration is *HBM-only*.
* Other way( Disable DRAM in BIOS): Enter BIOS and go through the following menu： EDKII Menu →  Socket Configuration →  Memory Configuration →  Memory DFX Configuration: 
    * DIMM Rank Enable Mask → Enable 
    * Socket 0 DDR Channel Mask → 0 
    * Socket 1 DDR Channel Mask → 0 
    * Socket 2 DDR Channel Mask → 0 
    * Socket 3 DDR Channel Mask → 0 

* No special OS config required to use HBM, but 
  * Use special caution to utilize limited HBM capacity
    * Minimize unnecessary services (drivers/daemons) 
    * Before each run consider:
      * Clearing file caches (if cached content is not useful) and compacting memory:  
          `sync; echo 3 > /proc/sys/vm/drop_caches; echo 1 >/proc/sys/vm/compact_memory`
      * Admins can provide scripts or include these in job prologue (setup) on batch systems
    * Reduce NUMA misses with zone_reclaim mode in Linux  
            `echo 2 > /proc/sys/vm/zone_reclaim_mode`

### *Flat （1LM）* Mode configuration
* Enter BIOS and go through the following menu：
         EDKII Menu →  Socket Configuration →  Memory Configurations →  Memory Map →  Volatile Memory Mode →  1LM

* HBM is ***not*** visible in default memory pool when booted into Linux
    * HBM is marked as special purpose memory in BIOS
      * Maximizes exclusive HBM capacity available for apps
      * Avoids unwanted OS usage of HBM (e.g., during boot)
    * Need additional `daxctl` commands on boot 
      * Install `daxctl` utilities
          `dnf install daxctl`
      * Use following commands to online HBM (for 2-socket system):
        * Use floowing in both *Quad* and *SNC4* mode
           ```
           daxctl reconfigure-device -m system-ram dax0.0
           daxctl reconfigure-device -m system-ram dax1.0
           ``` 
        * Use following only in *SNC4* mode
           ```
           daxctl reconfigure-device -m system-ram dax2.0
           daxctl reconfigure-device -m system-ram dax3.0 
           daxctl reconfigure-device -m system-ram dax4.0 
           daxctl reconfigure-device -m system-ram dax5.0 
           daxctl reconfigure-device -m system-ram dax6.0 
           daxctl reconfigure-device -m system-ram dax7.0
           ``` 
* After daxctl is used, we see both DDR and HBM
  * DDR nodes have cores, HBM nodes are memory only
  * Node order: DDR nodes followed by HBM nodes
    * 1-Socket: 
      * *Quad*: Node 0 is DDR with cores, Node 1 is HBM only
      * *SNC4*: Node 0-3 are DDR with cores, nodes 4-7 are HBM only
    * 2-Socket: 
      * *Quad*: Node 0-1 are DDR with cores, Nodes 2-3 are HBM only
      * *SNC4*: Node 0-7 are DDR with cores, 8-15 are HBM only

* By default, applications use DDR since DDR nodes have cores
    * Use numactl to place applications in HBM
          `numactl -m 8-15 ./app           # on 2S SNC4`

### *Cache（2LM）* Mode configuration
* Enter BISO and go through the following menu：
EDKII Menu →  Socket Configuration →  Memory Configurations →  Memory Map →  Volatile Memory Mode →  2LM

* HBM is transparent; only DDR is visible to software
  * Every LLC (L3) miss first goes to HBM cache
    * If misses in HBM cache, then accesses DDR

* No additional OS config required to use but …
  * Consider minimizing conflict misses for workloads that fit in cache
    * Use fake-NUMA Linux kernel boot option
      * numa=fake=nU          n = size of DDR / size of HBM

* Only DDR nodes are visible (HBM is transparent)
  * 1-Socket: 
    * *Quad*: Node 0 is DDR with cores
    * *SNC4*: Node 0-3 are DDR with cores
  * 2-Socket: 
    * *Quad*: Node 0-1 are DDR with cores
    * *SNC4*: Node 0-7 are DDR with cores

## SPR HBM clustering mode configuration
  If need config *SNC4* mode, please refer [setup-snc4.md][setup-snc4.md]


[setup-snc4.md]: setup-snc4.md