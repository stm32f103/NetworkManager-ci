import pytest

from ConnectionNMTest import ConnectionNMTest
from NMTest import NMTest

import NMcli
nmcli = NMcli.NMcli()

class TestConnection(ConnectionNMTest):

    def test_connection_help(self, com):
        keywords=["--active","id","uuid"]
        com.double_tab_after("nmcli con show ", keywords)
        keywords = ["autoconnect","con-name","help","ifname","type"]
        com.double_tab_after("nmcli con add ", keywords)
        keywords = ["add","down","help","modify","show","delete","edit","load","reload","up"]
        com.double_tab_after("nmcli con ", keywords)


    def test_connection_names_autocompletion(self, com):
        keywords = ["testeth0", "testeth6"]
        com.double_tab_after("nmcli con edit id ", keywords)
        self.not_double_tab_after("nmcli con edit id ", ["con_con"])
        nmcli.connection_add("con-name con_con type ethernet ifname eth5")
        com.double_tab_after("nmcli con edit id ", ["con_con"])
        com.double_tab_after("nmcli con edit ", ["con_con"])


    @pytest.mark.rhbz(1375933)
    def test_device_autocompletion(self, com):
        com.double_tab_after("mcli connection add type ethernet ifname ", ["eth0","eth2","eth10"])


    @pytest.mark.rhbz(1367736)
    def test_connection_objects_autocompletion(self, com):
        com.double_tab_after("nmcli connection add type bond -- ipv4.method manual ipv4.addresses 1.1.1.1/24 ip", ["ipv4.dad-timeout"])


    @pytest.mark.rhbz(1301226)
    def test_connection_objects_autocompletion(self, com):
        self.run_ver("+=1.4.0")
        com.double_tab_after("nmcli connection add type bond -- ipv4.method manual ipv4.addresses 1.1.1.1/24 ip", ["ipv4.dad-timeout"])


    def test_connection_double_delete(self):
        nmcli.connection_add("con-name con_con type ethernet ifname *")
        nmcli.connection_delete("con_con con_con")


    #def test_connection_autoconnect_yes(self, veth, editor):
    def test_connection_autoconnect_yes(self, editor, service):
        nmcli.connection_add("con-name con_con type ethernet ifname eth6")
        ed = editor.open("con_con")
        editor.send(ed, "set connection.autoconnect yes\n")
        editor.save(ed)
        editor.quit(ed)
        nmcli.connection_up("con_con") == 0
        nmcli.device_disconect("eth6")
        service.reboot()
        assert "con_con" in self.command_output("nmcli -t -f NAME  connection show -a", shell=True)
