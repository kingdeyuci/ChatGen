# Setup Storage

Certain workloads require to use data disk(s) as cache storage. The SUT workers must be equipped with the SSD or NVMe disks specified by the disk specification.

## Requesting disk storage

A workload can request data disk storage as follows:

- `HAS-SETUP-DISK-SPEC-1`: The worker node must have a set of SSD or NVMe disks, whose specification, `disk_spec_1`, is specified in the `cumulus` or `terraform` configuration files. The data disk is mount under `/mnt/diskN`, where `N` is the data disk count (starting from `1`).

## Node Labels

Label the worker nodes with the following node labels:

- `HAS-SETUP-DISK-SPEC-1=yes`: The worker node is equipped with the data storage disks described in `disk_spec_1`.

## Developer Note

The workload assumes full control over the `/mnt/diskN` content during the workload execution. This includes cleaning the content, at the start or completion of the workload execution. This makes it possible to share content across different runs.

> Special care must be taken not to take content under `/mnt/diskN` without checking version, completeness and integrity if the workload is designed to reuse the content across multiple runs.
