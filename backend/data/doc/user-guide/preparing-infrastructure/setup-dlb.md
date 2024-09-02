
# DLB Setup

DLB is supported in certain SPR SKUs. Please make sure your CPU sku (QDF) supports DLB.  

And DLB is broken with latest BKC kernel `5.15.0-spr.bkc.pc.2.10.0.x86_64`.
Before running the workload, please make sure your SPR has DLB device by running the following command:

```shell
lspci | grep 2710
```

If there are devices listed, then please download the zip file to your home folder: https://af01p-igk.devtools.intel.com/artifactory/platform_hero-igk-local/dlb_release_ver_7.5.0.zip

Execute the following commands:

```shell
unzip dlb_release_ver_7.5.0.zip
cd dlb/driver/dlb2/
make
sudo insmod dlb2.ko
```

Then you can run the workload on this machine.


## Node Labels

Setup the following node labels for DLB workloads:

- `HAS-SETUP-DLB=yes`: Must have.

## See Also

- [Hugepage Setup][Hugepage Setup]

[Hugepage Setup]: setup-hugepage.md

