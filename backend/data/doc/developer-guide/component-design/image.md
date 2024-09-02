# VM images

The document describes how to build VM images with [HashiCorp's Packer][packer.io]. The projects are located under the `image` directory.

## Prerequisites

If you haven't setup terraform, please follow the [instructions][instructions] to setup terraform for Cloud validation.

## CMakeLists.txt

Make the project depends on the `terraform` backend, and use the `add_image` function to declare the VM image project name as follows:

```cmake
if (BACKEND STREQUAL "terraform")
  add_image("my_vm_image")
endif()
```

## build.sh

In the `build.sh` script, you should specify the project variables and call the [`script/terraform/packer.sh`][packer.sh] script to build the VM images.

The `packer.sh` takes the following arguments:

```text
Usage: <project-name> $@
```

<!-- TODO: Extend above as it seems to be very vague (?) -->

The project name defines where the packer script location, expected to be under `template/packer/<csp>/<project-name>`, where `<csp>` is the Cloud Service Provider.

The script defines the following environment variables where you can include in your project definitions:
- **`OWNER`**: The owner string.
- **`REGION`**: The region string.
- **`ZONE`**: The availability zone string.
- **`NAMESPACE`**: The randomly generated namespace string of the current packer run.
- **`INSTANCE_TYPE`**: The CSP instance type.
- **`SPOT_INSTANCE`**: A boolean value to specify whether the build should use a spot instance.
- **`OS_DISK_TYPE`**: The OS disk type.
- **`OS_DISK_SIZE`**: The OS disk size.
- **`ARCHITECTURE`**: The architecture: `x86_64`, `amd64`, or `arm64`.
- **`SSH_PROXY_HOST`**: The socks5 proxy host name.
- **`SSH_PROXY_PORT`**: The socks5 proxy host port value.
- **`OS_IMAGE`**: The os_image value.

An example of `build.sh` may look like the following:

```shell
#!/bin/bash -e

COMMON_PROJECT_VARS=(
    'owner=$OWNER'
    'region=$REGION'
    'zone=$ZONE'
    'job_id=$NAMESPACE'
    'instance_type=$INSTANCE_TYPE'
    'spot_instance=$SPOT_INSTANCE'
    'os_disk_type=$OS_DISK_TYPE'
    'os_disk_size=$OS_DISK_SIZE'
    'architecture=$ARCHITECTURE'
    'ssh_proxy_host=$SSH_PROXY_HOST'
    'ssh_proxy_port=$SSH_PROXY_PORT'
    'image_name=wsf-${OS_TYPE}-${ARCHITECTURE}-dataset-ai'
    'ansible_playbook=../../../ansible/custom/install.yaml'
)

DIR="$( cd "$( dirname "$0" )" &> /dev/null && pwd )"
. "$DIR"/../../script/terraform/packer.sh generic $@
```

Optionally, you can also define CSP-specific variables, which will be merged with the common variables when running `packer.sh`:

```shell
AWS_PROJECT_VARS=(
    'subnet_id=$SUBNET_ID'
    'security_group_id=$SECURITY_GROUP_ID'
)

GCP_PROJECT_VARS=(
    'subnet_id=$SUBNET_ID'
    'project_id=$PROJECT_ID'
    'min_cpu_platform=$MIN_CPU_PLATFORM'
    'firewall_rules=$FIREWALL_RULES'
)

AZURE_PROJECT_VARS=(
    'subscription_id=$SUBSCRIPTION_ID'
    'availability_zone=$AVAILABILITY_ZONE'
    'network_name=$NETWORK_NAME'
    'subnet_name=$SUBNET_NAME'
    'managed_resource_group_name=$RESOURCE_GROUP_NAME'
)

ORACLE_PROJECT_VARS=(
    'subnet_id=$SUBNET_ID'
    'compartment=$COMPARTMENT'
    'cpu_core_count=$CPU_CORE_COUNT'
    'memory_size=$MEMORY_SIZE'
)

TENCENT_PROJECT_VARS=(
    'vpc_id=$VPC_ID'
    'subnet_id=$SUBNET_ID'
    'resource_group_id=$RESOURCE_GROUP_ID'
    'security_group_id=$SECURITY_GROUP_ID'
    'os_image_id=$OS_IMAGE_ID'
)

ALICLOUD_PROJECT_VARS=(
    'vpc_id=$VPC_ID'
    'resource_group_id=$RESOURCE_GROUP_ID'
    'security_group_id=$SECURITY_GROUP_ID'
    'vswitch_id=$VSWITCH_ID'
    'os_image_id=$OS_IMAGE_ID'
)

KVM_PROJECT_VARS=(
    'kvm_host=$KVM_HOST'
    'kvm_host_user=$KVM_HOST_USER'
    'kvm_host_port=$KVM_HOST_PORT'
    'pool_name=${KVM_HOST_POOL/null/osimages}' # Must exist
    'os_image=null'
)
```

The image building Ansible playbooks can also be applied directly to a static worker:

```shell
STATIC_PROJECT_VARS=(
    'ssh_port=$SSH_PORT'
    'user_name=$USER_NAME'
    'public_ip=$PUBLIC_IP'
    'private_ip=$PRIVATE_IP'
)
```

## Ansible playbooks

You should write custom installation scripts in Ansible playbooks, usually located under `template/ansible/<project-name>/install.yaml`. This location can be overwritten if you specify `ansible_playbook` in `build.sh`.

See [`basevm-generic`][basevm-generic] for an example of creating a `debian11` VM images with updated kernel 5.19.

More information about Ansible playbooks can be found in [Ansible playbooks documentation][ansible playbooks docs].

### Declare Ingredients in Ansible playbooks

Any component ingredients should be declared in `defaults/*.yaml` or `defaults/*.yml`:

```yaml
qpl_version: 1.28
qpl_repository: https://github.com/intel/qpl.git
```

where you can use the pairs of `_version` + `_package` or `_version` + `_repository`.

- `_version`, `_ver`: Declare the ingredient version.
- `_repository`, `_repo`: Declare the ingredient repository.
- `_package`, `_pkg`: Declare the package location.

> **Note:** The name of the variable is case-insensitive. Meaning, for example `_version` can be defined as `_VERSION`.

[instructions]: ../../user-guide/preparing-infrastructure/setup-terraform.md#setup-terraform-for-cloud-validation
[packer.sh]: ../../../script/terraform/packer.sh
[basevm-generic]: ../../../image/basevm-generic
[packer.io]: https://www.packer.io/
[ansible playbooks docs]: https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html