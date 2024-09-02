# Setup SNC4

SNC is an abbreviation for Sub-NUMA Clustering.

## Enable SNC
Change the BIOS setting as follows to enable SNC2/4:

```
EDKII Menu
  Socket Configuration
    Uncore Configuration
      Uncore General Configuration
        SNC: Enable SNC2 or Enable SNC4
```

## Check if SNC is enabled
To check if SNC4 is set or not:

```shell
lscpu | grep NUMA
```

With SNC4, you should see 8 NUMA nodes.  

