import pytest

from ConnectionNMTest import ConnectionNMTest
from NMTest import NMTest

con = ConnectionNMTest()


class TestConnection(ConnectionNMTest):

    def test_connection_help(self):
        #xxx
        keywords=["--active","id","uuid"]
        self.double_tab_after("nmcli con show ", keywords)

        keywords = ["autoconnect","con-name","help","ifname","type"]
        self.double_tab_after("nmcli con add ", keywords)

        keywords = ["add","down","help","modify","show","delete","edit","load","reload","up"]
        out = self.double_tab_after("nmcli con ", keywords)



    def test_connection_double_delete(self):
        assert self.nmcli_add_connection("con-name con_con type ethernet ifname *") == 0
        assert self.nmcli_delete_connection("con_con con_con") == 0
