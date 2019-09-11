import pytest

from NMTest import NMTest

from subprocess import call


class ConnectionNMTest(NMTest):

    @pytest.fixture(autouse=True)
    def con_con_remove(self):
        self.nmcli_delete_connection("con_con")
        yield
        self.nmcli_delete_connection("con_con")

    def nmcli_delete_connection(self, args):
        cmd = "nmcli connection delete " + args
        cmd = [ arg for arg in cmd.split(" ") if arg != "" ]
        return self.command_call(cmd)

    def nmcli_add_connection(self, args):
        cmd = "nmcli connection add " + args
        cmd = [ arg for arg in cmd.split(" ") if arg != "" ]
        return self.command_call(cmd)
