import pytest


class NMconfig:

    def __init__(self, service):
        self.service = service
        self.config_file="/etc/networkManager/conf.d/99-custom-xxx.conf"

    def clear(self):
        os.rm(self.config_file)

    def append(self, section, options):
        with open(self.config_file, "w+") as cf:
            cf.write("[%s]\n" % (section))
            for opt in options:
                cf.write("%s=%s\n" % (opt, options[opt]))

    def apply(self):
        self.service.restart_NM()

    def soft_apply(self):
        self.service.reload_NM()

@pytest.fixture()
def nmconfig(service, restart):
    c = NMconfig(service)
    yield c
    c.clear()
