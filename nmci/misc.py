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

    def test_version_tag_eval(self, ver_tags, version):

        # 1) the version tags '-'/'+' are just convenience forms of '-='/'+='. They
        #    need no special consideration ("+1.28.5" is exactly the same as "+=1.28.6").
        #
        # 2) if both '-=' and '+=' are present, then both groups must be satisfied
        #    at the same time. E.g. ver+=1.24,ver-=1.28 to define a range.
        #    That means, it evaluates
        #      (not has-minus or minus-satisfied) and (not has-plus or plus-satisfied)
        #
        # 3) for '+' group, the version tags are effectively OR-ed. Examples:
        #    - ver+=1.28.6 covers 1.28.6+ and 1.29+
        #    - ver+=1.28.6,ver+=1.30.4 covers 1.28.6+, 1.30.4+ and 1.31+, but does not cover 1.30.2
        #    - ver+=1.28.6,ver+1.30 covers 1.28.6+, 1.31+, but but does not cover 1.30.x
        #
        # 4) for '-' group, the version tags are effectively AND-ed. This is also to satisfy
        #    point 5). It makes sense, if you think about it.
        #
        # 5) '-' is the inverse of '+'. That is, "+=1.28.5" has the same meaning as "not(-1.28.5)".
        #    Or for example, if one test that specifies "ver+=1.28.6,ver+=1.29" and another
        #    "ver-1.28.6,ver-1.29", then they run never together.
        #    With De Morgan's laws we get "not(+=1.28.5 and +=1.30)"
        #                              == "not(not(-1.28.5) and not(-1.30))"
        #                              == "not(not(-1.28.5)) or not(not(-1.30))"
        #                              == "-1.28.5 or -1.30"

        l_version = len(version)
        assert l_version > 0
        assert all([v >= 0 for v in version])

        ver_tags = list(ver_tags)

        if not ver_tags:
            # no version tags means it's a PASS.
            return True

        for op, ver in ver_tags:
            assert op in ["+=", "+", "-=", "-"]
            assert all([type(v) is int and v >= 0 for v in ver])
            if len(ver) > l_version:
                raise ValueError(
                    'unexpectedly long version tag %s%s to compare "%s"'
                    % (op, ver, version)
                )

        # '+' is only a special case of '+=', and '-=' is only a special
        # case of '-'. Reduce the cases we have to handle.
        def _simplify_ver(op, ver):
            if op == "+":
                op = "+="
                ver = list(ver)
                ver[-1] += 1
            elif op == "-=":
                op = "-"
                ver = list(ver)
                ver[-1] += 1
            return (op, ver)

        ver_tags = [_simplify_ver(op, ver) for op, ver in ver_tags]

        def _eval(ver_tags, version):

            if not ver_tags:
                return None

            is_val_len_first = True

            for ver_len in range(1, len(version) + 1):

                ver_l = [ver for ver in ver_tags if len(ver) == ver_len]

                if not ver_l:
                    continue

                version_l = version[0:ver_len]

                ver_l.sort(reverse=True)

                has_match = False
                is_first = True
                for ver in ver_l:
                    m = ver <= version_l
                    if is_val_len_first:
                        if (
                            not is_first
                            and ver[0 : ver_len - 1] != version_l[0 : ver_len - 1]
                        ):
                            m = False
                    else:
                        if ver[0 : ver_len - 1] != version_l[0 : ver_len - 1]:
                            m = False

                    is_first = False
                    if m:
                        has_match = True
                        break

                if has_match:
                    return True

                is_val_len_first = False

            return False

        # See above: the '+' group gets OR-ed while the '-' group gets
        # AND-ed.  This is achieved by using the same _eval() call,
        # and then inverting @v2 (De Morgan's laws).
        v1 = _eval([ver for op, ver in ver_tags if op == "+="], version)
        v2 = _eval([ver for op, ver in ver_tags if op == "-"], version)

        if v2 is not None:
            v2 = not v2

        if v1 is None:
            v1 = True
        if v2 is None:
            v2 = True
        return v1 and v2

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
