import pytest
import subprocess, os

from NMTest import NMTest

# import nmcli with disabled assertions - connections does not have to exists in setup/teardown
import NMcli
nmcli = NMcli.NMcli(do_assert=False)


class AliasNMTest(NMTest):

    @pytest.fixture(autouse=True)
    def alias(self):
        nmcli.connection_up("testeth7")
        nmcli.connection_delete("eth7 ethernet-eth7")
        yield
        nmcli.connection_delete("eth7 ethernet-eth7")
        for i in range(3):
            if os.path.exists("/etc/sysconfig/network-scripts/ifcfg-eth7:%d" % i):
                os.remove("/etc/sysconfig/network-scripts/ifcfg-eth7:%d" % i)
        nmcli.connection_reload()
        nmcli.connection_down("testeth7")
