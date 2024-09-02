# Setup Calico VPP VCL

VPP Comms Library (VCL) is meant to simplify application integration with VPP by offering APIs that are similar to but not POSIX compliant.

## Installation

1. Install Kubernetes
2. Apply [`tigera-operator.yaml`][tigera-operator.yaml] with `kubectl create -f tigera-operator.yaml`
3. Apply [`installation-default.yaml`][installation-default.yaml] with
`kubectl create -f installation-default.yaml`
4. Apply [`calico-vpp.yaml`][calico-vpp.yaml]
    1. Please ensure you have configured sufficient hugepages
    2. Download [`calico-vpp.yaml`][calico-vpp.yaml]
    3. Modify `calico-vpp-config` `ConfigMap` part.
    Below is an example of `calico-vpp-config`. You need to replace `<interface-name>` with your own interface name.
        ```terraform
        apiVersion: v1
        data:
          CALICOVPP_CONFIG_TEMPLATE: |-
            unix {
              nodaemon
              full-coredump
              cli-listen /var/run/vpp/cli.sock
              pidfile /run/vpp/vpp.pid
              exec /etc/vpp/startup.exec
            }
            api-trace { on }
            cpu {
                main-core 0
                corelist-workers 1-4
            }
            socksvr {
                socket-name /var/run/vpp/vpp-api.sock
            }
            dpdk {
              dev __PCI_DEVICE_ID__ { num-rx-queues 1 num-tx-queues 1 tag main-<interface-name>}
            }
            session { enable use-app-socket-api }
            plugins {
                plugin default { enable }
                plugin dpdk_plugin.so { enable }
                plugin calico_plugin.so { enable }
                plugin ping_plugin.so { disable }
                plugin dispatch_trace_plugin.so { enable }
            }
            buffers {
              buffers-per-numa 131072
            }
          CALICOVPP_INITIAL_CONFIG: |-
            {
              "vppStartupSleepSeconds": 1,
              "corePattern": "/var/lib/vpp/vppcore.%e.%p"
            }
          CALICOVPP_INTERFACES: |-
            {
              "maxPodIfSpec": {
                "rx": 10, "tx": 10, "rxqsz": 1024, "txqsz": 1024
              },
              "defaultPodIfSpec": {
                "rx": 1, "tx":1, "isl3": true
              },
              "vppHostTapSpec": {
                "rx": 1, "tx": 1, "rxqsz": 1024, "txqsz": 1024, "isl3": false
              },
              "uplinkInterfaces": [
                {
                  "interfaceName": "<interface-name>",
                  "vppDriver": "dpdk",
                  "rxMode": "polling"
                }
              ]
            }
          CALICOVPP_FEATURE_GATES: |-
            {
              "memifEnabled": true,
              "vclEnabled": true,
              "multinetEnabled": false,
              "srv6Enabled": false,
              "ipsecEnabled": false
            }
          SERVICE_PREFIX: 10.96.0.0/12
        kind: ConfigMap
        metadata:
          name: calico-vpp-config
          namespace: calico-vpp-dataplane
        ```
      4. Execute the `kubectl create` to apply
          ```shell
          kubectl create -f calico-vpp.yaml
          ```

[tigera-operator.yaml]: https://raw.githubusercontent.com/projectcalico/calico/v3.25.1/manifests/tigera-operator.yaml
[installation-default.yaml]: https://raw.githubusercontent.com/projectcalico/vpp-dataplane/master/yaml/calico/installation-default.yaml
[calico-vpp.yaml]: https://raw.githubusercontent.com/projectcalico/vpp-dataplane/master/yaml/generated/calico-vpp.yaml
