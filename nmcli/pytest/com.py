import pytest
import subprocess, os, sys, pexpect

from time import sleep


class Command:
    def is_visible(self, command, pattern, seconds=2, check_type="default", exact_check=False, timeout=180, maxread=100000, interval=1):
        seconds = int(seconds)
        orig_seconds = seconds
        while seconds > 0:
            proc = pexpect.spawn('/bin/bash', ['-c', command], timeout = timeout, maxread=maxread, logfile=sys.stdout, encoding='utf-8')
            if exact_check:
                ret = proc.expect_exact([pattern, pexpect.EOF])
            else:
                ret = proc.expect([pattern, pexpect.EOF])
            if check_type == "default":
                if ret == 0:
                    return True
            elif check_type == "not":
                if ret != 0:
                    return True
            elif check_type == "full":
                assert ret == 0, 'Pattern "%s" disappeared after %d seconds, ouput was:\n%s' % (pattern, orig_seconds-seconds, proc.before)
            elif check_type == "not_full":
                assert ret != 0, 'Pattern "%s" appeared after %d seconds, output was:\n%s%s' % (pattern, orig_seconds-seconds, proc.before, proc.after)
            seconds = seconds - 1
            sleep(interval)
        if check_type == "default":
            assert 0, 'Did not see the pattern "%s" in %d seconds, output was:\n%s' % (pattern, orig_seconds, proc.before)
        elif check_type == "not":
            assert 0, 'Did still see the pattern "%s" in %d seconds, output was:\n%s%s' % (pattern, orig_seconds, proc.before, proc.after)


    def is_not_visible(self, command, pattern, seconds=2, check_type="default", exact_check=False, timeout=180, maxread=100000, interval=1):
        self.is_visible(command=command, pattern=pattern, seconds=seconds, check_type="not", exact_check=exact_check, timeout=timeout, maxread=maxread, interval=interval)

    def double_tab_after(self, command, keywords, timeout=2):
        os.system('echo "set page-completions off" > ~/.inputrc')
        os.system('echo "set completion-display-width 0" >> ~/.inputrc')
        exp = pexpect.spawn('/bin/bash', encoding='utf-8')
        exp.send(command)
        exp.sendcontrol('i')
        exp.sendcontrol('i')
        # copy list not to modify argument
        keywords = list(keywords)
        while len(keywords):
            ind = exp.expect([pexpect.TIMEOUT]+keywords, timeout=timeout)
            assert ind != 0, "did not see '%s'" % "|".join(keywords)
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
        assert ind == 0, "did see %s" % keywords[ind-1]
        exp.terminate(force=True)


@pytest.fixture()
def com():
    c = Command()
    yield c
