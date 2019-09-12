import pytest
import os
import subprocess
import pexpect

from subprocess import check_output,call
from datetime import datetime
from time import sleep

class NMTest:

    def _check_dump_package(self, pkg_name):
        if pkg_name in ["NetworkManager","ModemManager"]:
            return True
        return False


    def _embed_dump(self, dump_dir, dump_output, caption):
        print("Attaching %s, %s" % (caption, dump_dir))
        with open("/tmp/reported_crashes", "a") as f:
            f.write(dump_dir+"\n")
        with open("/tmp/last_crash", "w") as f:
            f.write(caption+"\n")
            f.write(dump_output)
        pytest.fail("Detected crash")


    def _list_dumps(self, dumps_search):
        p = subprocess.Popen("ls -d %s" % (dumps_search), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
        list_of_dumps, _ = p.communicate()
        return list_of_dumps.decode('utf-8').strip('\n').split('\n')


    @pytest.mark.order(-500)
    @pytest.fixture(autouse=True)
    def detect_faf(self):
        abrt_search = "/var/spool/abrt/ccpp*"
        list_of_dumps = self._list_dumps(abrt_search)
        for dump_dir in list_of_dumps:
            if not dump_dir:
                continue
            print("Examing crash: " + dump_dir)
            with open("%s/pkg_name" % (dump_dir), "r") as f:
                pkg = f.read()
            if not self._check_dump_package(pkg):
                continue
            with open("%s/last_occurrence" % (dump_dir), "r") as f:
                last_timestamp = f.read()
            # append last_timestamp, to check if last occurrence is reported
            if not self._is_dump_reported("%s-%s" % (dump_dir, last_timestamp)):
                with open("%s/reported_to" % (dump_dir), "r") as f:
                    reports = f.read().strip("\n").split("\n")
                url = ""
                for report in reports:
                    if "URL=" in report:
                        url = report.replace("URL=","")
                self._embed_dump("%s-%s" % (dump_dir ,last_timestamp), url, caption="FAF")


    @pytest.mark.order(-500)
    @pytest.fixture(autouse=True)
    def detect_coredump(self):
        coredump_search = "/var/lib/systemd/coredump/*"
        list_of_dumps = self._list_dumps(coredump_search)
        for dump_dir in list_of_dumps:
            if not dump_dir:
                continue
            print("Examing crash: " + dump_dir)
            dump_dir_split = dump_dir.split('.')
            if len(dump_dir_split) < 6:
                print("Some garbage in %s" % (dump_dir))
                continue
            if not self._check_dump_package(dump_dir_split[1]):
                continue
            try:
                pid, dump_timestamp = int(dump_dir_split[4]), int(dump_dir_split[5])
            except Exception as e:
                print("Some garbage in %s: %s" % (dump_dir, str(e)))
                continue
            if not self._is_dump_reported(dump_dir):
                p = subprocess.Popen('echo backtrace | coredumpctl debug %d' % (pid), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
                dump_output, _ = p.communicate()
                self._embed_dump(dump_dir, dump_output.decode('utf-8'), caption="COREDUMP")


    @pytest.mark.order(-400)
    @pytest.fixture(autouse=True)
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


    @pytest.mark.order(-98)
    @pytest.fixture(autouse=True)
    def output_state(self, request):
        self.dump_status("setup")
        yield
        self.dump_status("teardown")


    @pytest.mark.order(-97)
    @pytest.fixture(autouse=True)
    def nm_ver(self):
        print("NM_VER called")
        ver = self.command_output(['NetworkManager','--version'])
        print(ver)
        ver = ver.split("-")[0]
        self.NM_ver = self.get_ver_comparable(ver)
        print(self.NM_ver)
        yield

    def dump_status(self, when):
        print("=================================================================================")
        print("Network configuration %s:\n" % when)
        if self.command_call(['systemctl', 'status', 'NetworkManager'], log=None) != 0:
            for cmd in [['ip', 'addr'], ['ip', '-4', 'route'], ['ip','-6', 'route']]:
                print("--- %s ---" % " ".join(cmd))
                self.log.flush()
                self.command_call(cmd)
        else:
            for cmd in ['NetworkManager --version', 'ip addr', 'ip -4 route', 'ip -6 route',
                'nmcli g', 'nmcli c', 'nmcli d', 'nmcli -f IN-USE,SSID,CHAN,SIGNAL,SECURITY d w',
                'hostnamectl', 'NetworkManager --print-config', 'ps aux | grep dhclient']:
                print("--- %s ---" % cmd)
                self.command_call(cmd, shell=True)
            if os.path.isfile('/tmp/nm_newveth_configured'):
                print("\nVeth setup network namespace and DHCP server state:\n")
                for cmd in ['ip netns exec vethsetup ip addr', 'ip netns exec vethsetup ip -4 route',
                            'ip netns exec vethsetup ip -6 route', 'ps aux | grep dnsmasq']:
                    print("--- %s ---" % cmd)
                    self.command_call(cmd, shell=True)
        print("=================================================================================")

    # =================== steps ==============================
    def command_call(self, com, shell=False, log="std"):
        if not log:
            log_out = log_err = open(os.devnull, 'w')
        elif log == "std":
            return call(com, shell=shell)
        return call(com, shell=shell, stdout=log_out, stderr=log_err)


    def command_output(self, com, shell=False):
        return check_output(com, shell=shell).decode("utf-8")


    def command_error(self, com, shell=False):
        return check_output(com, stderr=subprocess.STDOUT, shell=shell).decode("utf-8")


    def popen(self, com, shell=False, timeout=15):
        p = subprocess.Popen(com, shell=shell, stdout=subprocess.PIPE, sterr=subprocess.PIPE, timeout=timeout)
        out, err = p.communicate()
        return out.decode("utf-8"), err.decode("utf-8")


    def command_expect(self, command, keywords):
        exp = pexpect.spawn('/bin/bash', encoding='utf-8')


    def get_ver_comparable(self, ver):
        ver_list = [ int(x) for x in ver.split('.') ]
        return ver_list


    def check_ver(self, ver_str):
        ver = ver_str.replace("-","").replace("+","").replace("=","")
        ver = self.get_ver_comparable(ver)
        if ver_str.startswith("+="):
            return self.NM_ver >= ver
        elif ver_str.startswith("-="):
            return self.NM_ver <= ver
        elif ver_str.startswith("+"):
            return self.NM_ver > ver
        elif ver_str.startswith("-"):
            return self.NM_ver > ver
        else:
            assert 0, "unable to parse version string '%s'" % ver_str


    def run_ver(self, ver_str):
        if not self.check_ver(ver_str):
            pytest.skip("incorrect NM version")
