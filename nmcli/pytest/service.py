import pytest
import subprocess

from time import sleep

from ip import IP
ip = IP(do_assert=False)

class Service:

    def restart_NM(self):
        self.restart("NetworkManager")

    def stop_NM(self):
        self.stop("NetworkManager")

    def restart_MM(self):
        self.restart("ModemManager")

    def restart(self, service):
        self._systemctl("restart", service)

    def stop(self, service):
        self._systemctl("stop", service)

    def reload(self, service):
        self._systemctl("reload", service)

    def reload_NM(self):
        self._reload("NetworkManager")

    def reload_MM(self):
        self._reload("ModemManager")

    def _systemctl(self, action, service):
        ret = subprocess.call(["sudo", "systemctl", action, service])
        assert ret == 0, "%s of %s failed" % (action, service)

    def reboot(self):
        self.stop_NM()
        for x in range(1,11):
            ip("link set dev eth%d down" % x, sudo=True)
            ip("addr flush dev eth%d" % x, sudo=True)

        ip("link set dev em2 down", sudo=True)
        ip("addr flush dev em2", sudo=True)

        ip("link del nm-bond")
        ip("link del nm-team")
        ip("link del team7")
        ip("link del bridge7")
        # for nmtui
        ip("link del bond0")
        ip("link del team0")


        subprocess.call("sudo rm -rf /var/run/NetworkManager", shell=True)

        sleep(1)
        self.restart_NM()
        sleep(2)


@pytest.fixture()
def service():
    s = Service()
    yield s


@pytest.fixture()
def restart(service):
    yield
    service.restart_NM()


@pytest.fixture()
def restart_before(service):
    service.restart_NM()
    yield


@pytest.fixture()
def restart_both(service):
    service.restart_NM()
    yield
    service.restart_NM()
