import subprocess

class IP:

    def __init__(self, do_assert=True, sudo=False):
        self.do_assert = do_assert
        self.sudo = sudo

    def __call__(self, command, do_assert=None, sudo=None):
        if do_assert is None:
            do_assert = self.do_assert
        if sudo is None:
            sudo = self.sudo

        command = "ip " + command
        if sudo:
            command = "sudo " + command
        args = [ arg for arg in command.split(" ") if arg != "" ]
        ret = subprocess.call(args)
        if do_assert:
            assert ret == 0, '"%s" failed' % command
        else:
            if ret != 0:
                print('"%s" failed' % command)
