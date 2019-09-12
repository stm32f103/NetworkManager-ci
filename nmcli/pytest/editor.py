import pytest
import pexpect
import subprocess
from time import sleep

class Editor:
    def __init__(self):
        pass

    def open(self, con_name):
        prompt = pexpect.spawn("nmcli connection ed %s" % (con_name), encoding="utf-8")
        r = prompt.expect([con_name, 'Error'])
        assert r != 1, 'Got an Error while opening profile %s\n%s%s' % (con_name, prompt.after, prompt.buffer)
        return prompt

    def open_with_timeout(self, con_name):
        prompt = pexpect.spawn('nmcli connection ed %s' % (con_name), maxread=6000, timeout=5, encoding='utf-8')
        sleep(2)
        context.prompt = prompt
        r = prompt.expect([con_name, 'Error'])
        assert r != 1, 'Got an Error while opening profile %s\n%s%s' % (con_name, prompt.after, prompt.buffer)
        return prompt

    def send(self, ed, what):
        ed.send(what)

    def send_backspace(self, ed):
        ed.send("\b")

    def clear_typed(self, ed):
        ed.send("\b"*128)

    def check_option_tab(self, ed, obj, options):
        ed.sendcontrol('c')
        ed.send('\n')
        send('set %s \t\t' % obj)
        sleep(0.25)
        options = list(options)
        while len(options):
            a =  context.prompt.expect([pexpect.TIMEOUT] + options, timeout=5)
            assert a != 0, "Options not shown: '%d'" % "|".join(options)

    def check_option_describe(self, ed, obj, options):
        ed.sendcontrol('c')
        ed.send('\n')
        sendline('describe %s' % obj)
        sleep(0.25)
        options = list(options)
        while len(options):
            a =  context.prompt.expect([pexpect.TIMEOUT] + options, timeout=5)
            assert a != 0, "Options not shown: '%d'" % "|".join(options)

    def check_succes_message(self, ed):
        ed.expect('successfully')

    def delete_connection_hit_enter(self, ed, name):
        subprocess.call(['nmcli','connection','delete','id', name])
        sleep(5)
        ed.send('\n')
        sleep(2)
        assert ed.isalive() is True, 'Something went wrong'

    def expect(self, ed, what, timeout=5):
        ed.expect(what, timeout=timeout)

    def quit(self, ed):
        ed.sendline("quit")
        sleep(0.3)

    def save(self, ed):
        ed.sendline('save')
        sleep(0.2)

@pytest.fixture()
def editor():
    ed = Editor()
    yield ed
