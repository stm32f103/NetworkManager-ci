#!/bin/bash
export PATH=/sbin:/bin:/usr/sbin:/usr/bin
exec >/dev/console 2>&1
export TERM=linux
export PS1='initramfs-test:\w\$ '

# load check library
dd if=/dev/sdb of=/check.sh
source /check.sh

echo "== nfs mounts =="
mount | grep nfs
echo "== ext3 mounts =="
mount | grep ext3

echo "== ls initrd ifcfg =="
ls -la /run/initramfs/state/etc/sysconfig/network-scripts

for file in $(find /run/initramfs/state/etc/sysconfig/network-scripts -type f); do
    echo "== $file =="
    cat $file
done

echo "== starting services =="
echo "import-state (to copy ifcfg files)"
systemctl start import-state.service || die "import-state failed: $(echo; systemctl status import-state.service)"
systemctl status import-state.service | cat
echo "dbus"
systemctl start dbus.service || die "dbus failed: $(echo; systemctl status dbus.service)"
systemctl status dbus.service | cat
echo "NetworkManager"
systemctl start NetworkManager.service || die "NetworkManager failed: $(echo; systemctl status NetworkManager.service)"
systemctl status NetworkManager.service | cat
echo "systemd-hostnamed"
systemctl start systemd-hostnamed.service || die "systemd-hostnamed failed: $(echo; systemctl status systemd-hostnamed.service)"
systemctl status systemd-hostnamed.service | cat
echo "OK"

echo "== ls ifcfg =="
ls -la /etc/sysconfig/network-scripts/

for file in $(find /etc/sysconfig/network-scripts/ -type f); do
    echo "== $file =="
    cat $file
done

echo "== ip addr =="
ip addr
echo "== ip -4 route =="
ip -4 route
echo "== ip -6 route =="
ip -6 route

echo "== nmcli device =="
nmcli device | cat
echo "== nmcli connection =="
nmcli con | cat

client_check

# client_check should "die" if failed
echo PASS | dd oflag=direct,dsync of=/dev/sda

# cleanup after succes
clean_root

poweroff -f