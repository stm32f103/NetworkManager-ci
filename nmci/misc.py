import os
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

    def test_get_feature_files(self, feature):

        import glob

        if feature[0] == "/":
            feature_dir = os.path.join(feature, "features")
        else:
            feature_dir = util.base_dir(feature, "features")

        return glob.glob(feature_dir + "/*.feature")

    def test_load_tags_from_features(self, feature, test_name=None):

        files = self.test_get_feature_files(feature)
        if not files:
            return []

        def _split_line(line):

            # replace tabs with spaces.
            line = line.replace("\t", " ")

            # trim at the first '#' (which indicates a comment).
            i = line.find("#")
            if i != -1:
                line = line[0:i]

            words = line.split(" ")

            # remove empty tokens.
            words = [w for w in words if w]

            return words

        test_tags = subprocess.check_output(
            [
                "awk",
                "--",
                """
                    BEGIN {ORS=\" \"}
                    /^\\s*@/ { print $0 }
                    /^\\s*Scenario/ { print \"\\n\" }
                """,
                *files,
            ]
        )
        test_tags = test_tags.decode("utf-8", "error")
        test_tags = test_tags.split("\n")
        test_tags = [_split_line(line) for line in test_tags]
        test_tags = [line for line in test_tags if line]

        rr = re.compile("^@" + self.TEST_NAME_VALID_CHAR_REGEX + "+$")
        for line in test_tags:
            if not all((rr.match(s) for s in line)):
                raise ValueError("unexpected characters in tags: %s" % (line))

        test_tags = [[s[1:] for s in line] for line in test_tags]
        if test_name is not None:
            test_tags = [line for line in test_tags if test_name in line]
        return test_tags

    def test_version_tag_parse(self, version_tag, tag_candidate):

        if not version_tag.startswith(tag_candidate):
            raise ValueError(
                f'tag "{version_tag}" does not start with "{tag_candidate}"'
            )

        version_tag = version_tag[len(tag_candidate) :]

        if version_tag.startswith("+=") or version_tag.startswith("-="):
            op = version_tag[0:2]
            ver = version_tag[2:]
        elif version_tag.startswith("+") or version_tag.startswith("-"):
            op = version_tag[0:1]
            ver = version_tag[1:]
        else:
            raise ValueError(
                f'tag "{version_tag}" does not have a suitable "+-" part for "{tag_candidate}"'
            )

        if not re.match("^[0-9.]+$", ver):
            raise ValueError(
                'tag "{version_tag}" does not have a suitable version number for "{tag_candidate}"'
            )

        ver_arr = [int(x) for x in ver.split(".")]
        return (op, ver_arr)

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
