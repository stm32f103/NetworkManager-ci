# -*- coding: UTF-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from behave import step
import sys
import os
import subprocess


def utf_only_open_read(file, mode='r'):
    # Opens file and read it w/o non utf-8 chars
    if sys.version_info.major < 3:
        return open(file, mode).read().decode('utf-8', 'ignore').encode('utf-8')
    else:
        return open(file, mode, encoding='utf-8', errors='ignore').read()


@step(u'Run dracut test')
def dracut_run(context):
    qemu_args = ""
    kernel_args = "rd.net.timeout.dhcp=10 panic=1 systemd.crash_reboot rd.shell=0 rd.debug loglevel=7 " \
                  "rd.retry=50 console=ttyS0,115200n81 noapic "
    #kernel_args = "rd.net.timeout.dhcp=3 panic=1 systemd.crash_reboot rd.shell=0 " \
    initrd = "initramfs.client.NM"
    checks = ""
    timeout = "8m"
    ram = "768"
    log_contains = []
    log_not_contains = []
    test_type = "nfs"
    for row in context.table:
        if "qemu" in row[0].lower():
            qemu_args += " " + row[1]
        elif "kernel" in row[0].lower():
            kernel_args += " " + row[1]
        elif "initrd" in row[0].lower():
            initrd = row[1]
        elif "check" in row[0].lower():
            checks += row[1] + " || die '" + '"' + row[1] + '"' + " failed'\n"
        elif "log+" in row[0].lower():
            log_contains.append(row[1])
        elif "log-" in row[0].lower():
            log_not_contains.append(row[1])
        elif "type" in row[0].lower():
            test_type = row[1]
        elif "timeout" in row[0].lower():
            timeout = row[1]
        elif "ram" in row[0].lower():
            ram = row[1]

    with open("/tmp/client-check.sh", "w") as f:
        f.write("client_check() {\n" + checks + "}")

    rc = subprocess.call(
        "cd contrib/dracut/; . ./setup.sh; "
        "echo NONE > $TESTDIR/client.img; "
        "cat check_lib/*.sh /tmp/client-check.sh > $TESTDIR/client_check.img; "
        "RAM=%s timeout %s bash ./run-qemu "
        "-drive format=raw,index=0,media=disk,file=$TESTDIR/client.img "
        "-drive format=raw,index=1,media=disk,file=$TESTDIR/client_check.img "
        "%s -append \"%s\" -initrd $TESTDIR/%s "
        "&> /tmp/dracut_boot.log " % (ram, timeout, qemu_args, kernel_args, initrd), shell=True)

    result = "NO_BOOT"
    if os.path.isfile("/tmp/dracut_test/client.img"):
        result = utf_only_open_read("/tmp/dracut_test/client.img")

    if "PASS" not in result and os.path.isfile("/tmp/dracut_boot.log"):
        boot_log = utf_only_open_read("/tmp/dracut_boot.log")
        context.embed("text/plain", boot_log, "DRACUT_BOOT")

    if not result.startswith("NO"):
        logs = {}
        logs["DRACUT_TEST"] = "-u testsuite"
        if "PASS" not in result:
            logs["DRACUT_NM"] = "-u NetworkManager -o cat"
        log_cmd = " ".join(["/tmp/%s.log '%s'" % (x, logs[x]) for x in logs])
        log_cmd = "bash contrib/dracut/get_log.sh " + test_type + " " + log_cmd
        proc = subprocess.run(log_cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")

        if proc.returncode != 0:
            msg = "Error during log collection\nretcode:%d\noutput:%s" \
                % (proc.returncode, str(proc.stdout))
            context.embed("text/plain", msg, "DRACUT_LOGS_ERROR")
        else:
            for log in logs:
                log_f = "/tmp/" + log + ".log"
                if os.path.isfile(log_f):
                    context.embed("text/plain", utf_only_open_read(log_f) + "\n", log)
                    subprocess.call("rm -rf " + log_f, shell=True)
                else:
                    msg = "Error: log file '" + log_f + "' was not created for some reason"
                    context.embed("text/plain", msg, log)
        if proc.stdout is not None:
            context.embed("text/plain", proc.stdout, "DRACUT_LOG_COLLECTOR")
    assert rc == 0, f"Test run FAILED, VM returncode: {rc}, VM result: {result}"
    assert "PASS" in result, f"Test FAILED, VM result: {result}"

    for log_line in log_contains:
        assert log_line in boot_log, "Fail: not visible in log:\n" + log_line
    for log_line in log_not_contains:
        assert log_line not in boot_log, "Fail: visible in log:\n" + log_line
