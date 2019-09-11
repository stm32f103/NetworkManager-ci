import pytest
import os
import subprocess
import pexpect

from subprocess import check_output,call
from datetime import datetime

class NMTest:

    log = None

    @pytest.mark.order(-100)
    @pytest.fixture(autouse=True, )
    def capture_NM_log(self):
        t_start = datetime.now()
        log_cursor_raw = self.command_output(["sudo", "journalctl", "--lines=0", "--show-cursor"])
        for log_line in log_cursor_raw.split("\n"):
            if "cursor:" in log_line:
                self.log_cursor = '--cursor=%s' % log_line.replace("-- cursor: ", "").strip()
        yield
        with open('/tmp/journal-nm.log', "w") as nm_log:
            import time
            nm_log.write('~~~~~~~~~~~~~~~~~~~~~~~~~~ NM LOG ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
            cmd = ["sudo", "journalctl", "-all", "-u", "NetworkManager", "--no-pager", "-o", "cat", self.log_cursor]
            data = self.command_output(cmd)
            if len(data) > 20000000:
                data = "WARNING: 20M size exceeded in /tmp/journal-nm.log, skipping"
                print(raw(escape()))
            nm_log.write(data)
        t_end = datetime.now()
        with open('/tmp/test_duration', "w") as f:
            f.write(str(t_end - t_start))


    @pytest.mark.order(-99)
    @pytest.fixture(autouse=True)
    def catch_faf_crash(self):
        pass

    @pytest.mark.order(-98)
    @pytest.fixture(autouse=True)
    def output_state(self, request):
        self.log = open("/tmp/main-nm.log", "w")
        self.dump_status("setup")
        yield
        self.dump_status("teardown")
        self.log.close()

    def dump_status(self, when):
        print("=================================================================================\n")
        print("Network configuration %s:\n\n" % when)
        if self.command_call(['systemctl', 'status', 'NetworkManager'], log=None) != 0:
            for cmd in [['ip', 'addr'], ['ip', '-4', 'route'], ['ip','-6', 'route'], ['ls', 'x']]:
                print("--- %s ---\n" % cmd)
                self.log.flush()
                self.command_call(cmd)
        else:
            for cmd in ['NetworkManager --version', 'ip addr', 'ip -4 route', 'ip -6 route',
                'nmcli g', 'nmcli c', 'nmcli d', 'nmcli -f IN-USE,SSID,CHAN,SIGNAL,SECURITY d w',
                'hostnamectl', 'NetworkManager --print-config', 'ps aux | grep dhclient']:
                print("--- %s ---\n" % cmd)
                self.command_call(cmd, shell=True)
            if os.path.isfile('/tmp/nm_newveth_configured'):
                print("\nVeth setup network namespace and DHCP server state:\n")
                for cmd in ['ip netns exec vethsetup ip addr', 'ip netns exec vethsetup ip -4 route',
                            'ip netns exec vethsetup ip -6 route', 'ps aux | grep dnsmasq']:
                    print("--- %s ---\n" % cmd)
                    self.command_call(cmd, shell=True)
        print("=================================================================================\n")

    # =================== steps ==============================
    def command_call(self, com, shell=False, log="std"):
        if log == "log":
            log_out = log_err = self.log
        elif not log:
            log_out = log_err = open(os.devnull, 'w')
        elif log == "std":
            return call(com, shell=shell)
        return call(com, shell=shell, stdout=log_out, stderr=log_err)

    def command_output(self, com, shell=False):
        return check_output(com, shell=shell).decode("utf-8")

    def command_error(self, com, shell=False):
        return check_output(com, stderr=subprocess.STDOUT, shell=shell).decode("utf-8")

    def popen(self, com, shell=False, timeout=15):
        p = Popen(com, shell=shell, stdout=subprocess.PIPE, sterr=subprocess.PIPE, timeout=timeout)
        out, err = p.communicate()
        return out.decode("utf-8"), err.decode("utf-8")

    def command_expect(self, command, keywords):
        exp = pexpect.spawn('/bin/bash', encoding='utf-8')

    def double_tab_after(self, command, keywords, timeout=2):
        os.system('echo "set page-completions off" > ~/.inputrc')
        os.system('echo "set completion-display-width 0" >> ~/.inputrc')
        exp = pexpect.spawn('/bin/bash', encoding='utf-8')
        exp.send(command)
        exp.sendcontrol('i')
        exp.sendcontrol('i')
        while len(keywords):
            ind = exp.expect([pexpect.TIMEOUT]+keywords, timeout=timeout)
            assert ind != 0, "did not see %s" % keywords[ind]
            keywords.pop(ind-1)
        exp.terminate(force=True)

    def not_double_tab_after(self, command, keywords, timeout=2):
        os.system('echo "set page-completions off" > ~/.inputrc')
        os.system('echo "set completion-display-width 0" >> ~/.inputrc')
        exp = pexpect.spawn('/bin/bash', encoding='utf-8')
        exp.send(command)
        exp.sendcontrol('i')
        exp.sendcontrol('i')
        ind = exp.expect([pexpect.TIMEOUT]+keywords, timeout=timeout)
        assert ind == 0, "did see %s" % keywords[ind]
        exp.terminate(force=True)
