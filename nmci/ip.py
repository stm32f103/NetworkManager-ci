import sys
import subprocess

from . import util


class _IP:
    def link_show(self, ifindex=None, ifname=None):

        # We require valid UTF-8 output. That means, you cannot use this
        # function if you add interfaces with a non-UTF-8 name.
        #
        # And of course, in those cases `iproute2` wouldn't even output valid
        # json to begin with, because json can only be UTF-8.
        jstr = util.process_run(
            ["ip", "-j", "-d", "link", "show"], as_utf8=True, timeout=2
        )

        import json

        result = []
        for data in json.loads(jstr):
            ii = data["ifindex"]
            if ifindex is not None and int(ifindex) != ii:
                continue
            ii = data["ifname"]
            if ifname is not None and ifname != ii:
                continue
            result.append(data)

        if ifindex is not None or ifname is not None:

            # If the users asks for a certain ifindex/ifname, then we require
            # to find exactly one interface. Otherwise, we will fail.
            if len(result) != 1:
                if ifindex is None:
                    s = 'ifname="%s"' % (ifname)
                elif ifname is None:
                    s = "ifindex=%s" % (ifindex)
                else:
                    s = 'ifindex=%s, ifname="%s"' % (ifindex, ifname)
                if not result:
                    raise KeyError("Could not find interface with " + s)
                raise KeyError("Could not find unique interface with " + s)

            # Beware: in this mode we don't return an array of length 0.
            # We directly return the found dictionary.
            return result[0]

        return result


sys.modules[__name__] = _IP()
