#!/bin/bash
set -e

NM_CI_DIR=$1
cd $NM_CI_DIR
shift 1

cmd=$1
shift 1

if [ "$cmd" == "install" ]; then
    if ! [ -f /tmp/network_pkgs_installed ]; then
        set -x
        yum -y install NetworkManager-libreswan-gnome NetworkManager-libreswan
        yum -y install NetworkManager-openvpn-gnome NetworkManager-openvpn \
        || yum -y install \
          https://kojipkgs.fedoraproject.org//packages/NetworkManager-openvpn/1.8.10/1.fc30/x86_64/NetworkManager-openvpn-1.8.10-1.fc30.x86_64.rpm \
          https://kojipkgs.fedoraproject.org//packages/NetworkManager-openvpn/1.8.10/1.fc30/x86_64/NetworkManager-openvpn-gnome-1.8.10-1.fc30.x86_64.rpm
        pip3 install proxy.py
        systemctl restart NetworkManager
        touch /tmp/network_pkgs_installed
        set +x
    fi
elif [ "$cmd" == "envsetup" ]; then
    cp /etc/shadow /etc/shadow.backup
    bash -x prepare/envsetup.sh setup "$@"
    mv /etc/shadow.backup /etc/shadow
else
    chmod +x "$cmd"
    set -x
    ./$cmd "$@"
    set +x
fi
