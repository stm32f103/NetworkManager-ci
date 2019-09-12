import pexpect

class NMcli:

    def __init__(self, do_assert=True):
        self.do_assert = do_assert

    def _nmcli(self, cmd, timeout=5):
        cli = pexpect.spawn(cmd, timeout=timeout, encoding='utf-8')
        r = cli.expect(['Error', pexpect.TIMEOUT, pexpect.EOF])
        r2 = cli.expect([pexpect.EOF, pexpect.TIMEOUT], timeout=180)
        if self.do_assert:
            assert r != 0, 'error in "%s":\n%s%s' % (cmd, cli.after, cli.buffer)
            assert r != 1, '"%s" timed out (%ds)' % (cmd, timeout)
        else:
            if r == 0:
                print('error in "%s":\n%s%s' % (cmd, cli.after, cli.buffer))
            elif r == 1:
                print('"%s" timed out (%ds)' % (cmd, timeout))
        assert r2 == 0, '"%s" hanged !!!' % (cmd)

    def connection_add(self, args, timeout=5):
        self._nmcli("nmcli con add %s" % args, timeout=timeout)

    def connection_delete(self, conn, timeout=5):
        self._nmcli("nmcli con del %s" % conn, timeout=timeout)

    def connection_up(self, conn, timeout=10):
        self._nmcli("nmcli con up %s" % conn, timeout=timeout)

    def connection_down(self, conn, timeout=10):
        self._nmcli("nmcli con down %s" + conn, timeout=timeout)

    def device_disconect(self, device, timeout=180):
        self._nmcli("nmcli device disconnect %s" % device, timeout=timeout)
