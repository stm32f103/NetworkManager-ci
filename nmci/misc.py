import re
import subprocess
import sys

from . import ip
from . import sdresolved
from . import util


class _Misc:

    TEST_NAME_VALID_CHAR_REGEX = "[-a-z_.A-Z0-9+=]"

    def test_name_normalize(self, test_name):
        test_name0 = test_name
        m = re.match("^[^_]*NetworkManager[^_]*_[^_]*Test[^_]*_(.*)$", test_name)
        if m:
            test_name = m.group(1)
        if test_name[0] == "@":
            test_name = test_name[1:]
        if not re.match("^" + self.TEST_NAME_VALID_CHAR_REGEX + "+$", test_name):
            raise ValueError(f"Invalid test name {test_name0}")
        return test_name

    def nmlog_parse_dnsmasq(self, ifname):
        s = util.process_run(
            [util.util_dir("helpers/nmlog-parse-dnsmasq.sh"), ifname], as_utf8=True
        )
        import json

        return json.loads(s)

    def get_dns_info(self, dns_plugin, ifindex=None, ifname=None):

        if ifindex is None and ifname is None:
            raise ValueError("Missing argument, either ifindex or ifname must be given")

        ifdata = ip.link_show(ifindex=ifindex, ifname=ifname)

        if dns_plugin == "dnsmasq":
            info = self.nmlog_parse_dnsmasq(ifdata["ifname"])
            info["default_route"] = any((s == "." for s in info["domains"]))
            info["domains"] = [(s, "routing") for s in info["domains"]]
        elif dns_plugin == "systemd-resolved":
            info = sdresolved.link_get_all(ifdata["ifindex"])
            pass
        else:
            raise ValueError('Invalid dns_plugin "%"' % (dns_plugin))

        info["dns_plugin"] = dns_plugin
        return info


sys.modules[__name__] = _Misc()
