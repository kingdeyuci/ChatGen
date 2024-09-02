# Setup 5G environment

This document is a guide for setting up the HW & SW config for build up the 5G environment for benchmark.

## Smart Edge Open DEK Setup

1. Follow the [wiki][wiki] to install Smart Edge environment.
2. Add `multus-cni` on DEK. Please see [`multus-cni` setup][multus-cni setup] for instructions.

## Network Setup

1. Use two 100GE copper(or optical) cables to connect those 100GE ports, connection method:
    ```text
    Host0 100GE physical port0 <-> Host1 100GE physical port0;
    (100GE connection 0 between two Linux hosts)

    Host0 100GE physical port1 <-> Host1 100GE physical port1;
    (100GE connection 1 between two Linux hosts)
    ```
    > Note: Make sure those 100GE ports is link up from NIC ports LED green light after machine power on again.

2. Use ifconfig command to config correct IP address with two different subnets (e.g. 6.6.6.x and 7.7.7.x) for two 100GE connections, ping each other Linux Host to make sure those 100GE connections works fine.
e.g., you can configure IP address like this:
    ```text
    Host0 100GE physical port0(6.6.6.3) <-> Host1 100GE physical port0(6.6.6.4).
    Host0 100GE physical port1(7.7.7.3) <-> Host1 100GE physical port1(7.7.7.4).
    ```

    - Host0
        ```shell
        sudo ifconfig <port0-name> 6.6.6.3 netmask 255.255.255.0 up
        sudo ifconfig <port1-name> 7.7.7.3 netmask 255.255.255.0 up
        ip route add 6.6.6.0/24 dev <port0-name>
        ip route add 7.7.7.0/24 dev <port1-name>
        ```
    - Host1
        ```shell
        sudo ifconfig <port0-name> 6.6.6.4 netmask 255.255.255.0 up
        sudo ifconfig <port1-name> 7.7.7.4 netmask 255.255.255.0 up
        ip route add 6.6.6.0/24 dev <port0-name>
        ip route add 7.7.7.0/24 dev <port1-name>
        ip route add default via 6.6.6.6 dev <port0-name> metric 200
        ip route add default via 7.7.7.6 dev <port1-name> metric 201
        ```
    - Host0
        ```shell
        ping 6.6.6.4
        ping 7.7.7.4
        ```

3. Generate the SSL certificates in the etc directory.
    ```shell
    cd /etc
    openssl genrsa -out server.key 3072
    openssl req -new -key server.key -out server.csr (input user info)
    openssl x509 -req -in server.csr -out server.crt -signkey server.key -days 3650
    ```

4. Create a configuration file named `network_env.conf` in the etc directory. This file contains the NIC and server ip information. The context should follow the following format: `/etc/network_env.conf`
    ```conf
    gma_client_5g_interface=ens801f1
    gma_client_wifi_interface=ens801f0
    server_ncm_ip=7.7.7.6
    ```
    - `gma_client_5g_interface` means 5g NIC port name.
    - `gma_client_wifi_interface` means wifi NIC port name.
    - `server_ncm_ip` means gma server ncm service ip address and is set to `7.7.7.6` by default.

## Node Labels
Label the the worker node(s) with the following label:
- `HAS-SETUP-5G=yes`

## See Also
[Intel® Smart Edge Open Developer Experience Kit – Default Installation Instructions][Intel Smart Edge Open Developer Experience Kit]

[wiki]: https://wiki.ith.intel.com/display/wiechina/Smart+Edge+Open+Developer+Experience+Kits+Deployment
[multus-cni setup]: https://github.com/k8snetworkplumbingwg/multus-cni/blob/master/docs/quickstart.md
[Intel Smart Edge Open Developer Experience Kit]: https://www.intel.com/content/www/us/en/developer/articles/reference-implementation/smart-edge-open-developer-experience-kit.html