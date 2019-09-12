import pytest

from NMTest import NMTest

# import nmcli with disabled assertions - connections does not have to exists in setup/teardown
import NMcli
nmcli = NMcli.NMcli(do_assert=False)

from subprocess import call


class ConnectionNMTest(NMTest):

    @pytest.fixture(autouse=True)
    def con_con_remove(self):
        nmcli.connection_delete("con_con con_con2")
        yield
        nmcli.connection_delete("con_con con_con2")
