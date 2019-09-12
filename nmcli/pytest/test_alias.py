import pytest
import os

from AliasNMTest import AliasNMTest
from NMTest import NMTest

import NMcli
nmcli = NMcli.NMcli()

class TestAlias(AliasNMTest):

    def test_alias_ifcfg_add_single_alias(self, com):
        nmcli.connection_add("type ethernet ifname eth7 con-name eth7 autoconnect yes ipv4.may-fail no ipv4.method manual ipv4.addresses 192.168.0.100/24 ipv4.gateway 192.168.0.1")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:0", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:0'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.101\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        nmcli.connection_reload()
        nmcli.connection_up("eth7")
        com.is_visible("ip a s eth7", "inet 192.168.0.101")
        com.is_visible("ip a s eth7", "inet 192.168.0.100")


    def test_alias_ifcfg_add_multiple_aliases(self, com):
        nmcli.connection_add("type ethernet ifname eth7 con-name eth7 autoconnect yes ipv4.may-fail no ipv4.method manual ipv4.addresses 192.168.0.100/24 ipv4.gateway 192.168.0.1")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:0", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:0'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.101\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:1", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:1'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.102\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:2", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:2'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.103\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        nmcli.connection_reload()
        nmcli.connection_up("eth7")
        com.is_visible("ip a s eth7", "inet 192.168.0.100")
        com.is_visible("ip a s eth7", "inet 192.168.0.101")
        com.is_visible("ip a s eth7", "inet 192.168.0.102")
        com.is_visible("ip a s eth7", "inet 192.168.0.103")


    def test_alias_ifcfg_connection_restart(self, com):
        nmcli.connection_add("type ethernet ifname eth7 con-name eth7 autoconnect yes ipv4.may-fail no ipv4.method manual ipv4.addresses 192.168.0.100/24 ipv4.gateway 192.168.0.1")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:0", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:0'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.101\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:1", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:1'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.102\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:2", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:2'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.103\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        nmcli.connection_reload()
        nmcli.connection_up("eth7")
        nmcli.connection_down("eth7")
        nmcli.connection_up("eth7")
        com.is_visible("ip a s eth7", "inet 192.168.0.100")
        com.is_visible("ip a s eth7", "inet 192.168.0.101")
        com.is_visible("ip a s eth7", "inet 192.168.0.102")
        com.is_visible("ip a s eth7", "inet 192.168.0.103")


    def test_alias_ifcfg_remove_single_alias(self, com):
        nmcli.connection_add("type ethernet ifname eth7 con-name eth7 autoconnect yes ipv4.may-fail no ipv4.method manual ipv4.addresses 192.168.0.100/24 ipv4.gateway 192.168.0.1")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:0", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:0'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.101\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:1", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:1'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.102\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:2", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:2'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.103\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        nmcli.connection_reload()
        nmcli.connection_up("eth7")
        os.remove("/etc/sysconfig/network-scripts/ifcfg-eth7:0")
        nmcli.connection_reload()
        nmcli.connection_up("eth7")
        com.is_visible("ip a s eth7", "inet 192.168.0.100")
        com.is_not_visible("ip a s eth7", "inet 192.168.0.101")
        com.is_visible("ip a s eth7", "inet 192.168.0.102")
        com.is_visible("ip a s eth7", "inet 192.168.0.103")


    def test_alias_ifcfg_remove_all_aliases(self, com):
        nmcli.connection_add("type ethernet ifname eth7 con-name eth7 autoconnect yes ipv4.may-fail no ipv4.method manual ipv4.addresses 192.168.0.100/24 ipv4.gateway 192.168.0.1")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:0", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:0'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.101\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:1", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:1'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.102\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:2", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:2'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.103\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        nmcli.connection_reload()
        nmcli.connection_up("eth7")
        os.remove("/etc/sysconfig/network-scripts/ifcfg-eth7:0")
        os.remove("/etc/sysconfig/network-scripts/ifcfg-eth7:1")
        os.remove("/etc/sysconfig/network-scripts/ifcfg-eth7:2")
        nmcli.connection_reload()
        nmcli.connection_up("eth7")
        com.is_visible("ip a s eth7", "inet 192.168.0.100")
        com.is_not_visible("ip a s eth7", "inet 192.168.0.101")
        com.is_not_visible("ip a s eth7", "inet 192.168.0.102")
        com.is_not_visible("ip a s eth7", "inet 192.168.0.103")


    def test_alias_ifcfg_reboot(self, com, service, restart):
        nmcli.connection_add("type ethernet ifname eth7 con-name eth7 autoconnect yes ipv4.may-fail no ipv4.method manual ipv4.addresses 192.168.0.100/24 ipv4.gateway 192.168.0.1")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:0", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:0'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.101\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:1", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:1'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.102\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        with open("/etc/sysconfig/network-scripts/ifcfg-eth7:2", "a") as ifcfg:
            ifcfg.write("DEVICE='eth7:2'\n")
            ifcfg.write("GATEWAY=192.168.0.1\n")
            ifcfg.write("IPADDR=192.168.0.103\n")
            ifcfg.write("NETMASK=255.255.255.0\n")
        nmcli.connection_reload()
        nmcli.connection_up("eth7")
        service.reboot()
        com.is_visible("ip a s eth7", "inet 192.168.0.100")
        com.is_visible("ip a s eth7", "inet 192.168.0.101")
        com.is_visible("ip a s eth7", "inet 192.168.0.102")
        com.is_visible("ip a s eth7", "inet 192.168.0.103")
