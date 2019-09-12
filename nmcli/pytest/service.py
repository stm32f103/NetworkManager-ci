import pytest
import subprocess


class Service:

    def restart_NM(self):
        self.restart("NetworkManager")

    def restart_MM(self):
        self.restart("ModemManager")

    def restart(self, service):
        self._systemctl("restart", service)

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
            subprocess.call("sudo ip link set dev eth%d down" %int(x), shell=True)
            subprocess.call("sudo ip addr flush dev eth%d" %int(x), shell=True)

        subprocess.call("sudo ip link set dev em2 down", shell=True)
        subprocess.call("sudo ip addr flush dev em2", shell=True)

        subprocess.call("ip link del nm-bond", shell=True)
        subprocess.call("ip link del nm-team", shell=True)
        subprocess.call("ip link del team7", shell=True)
        subprocess.call("ip link del bridge7", shell=True)
        # for nmtui
        subprocess.call("ip link del bond0", shell=True)
        subprocess.call("ip link del team0", shell=True)


        subprocess.call("rm -rf /var/run/NetworkManager", shell=True)

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
