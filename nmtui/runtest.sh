#!/bin/bash
set -x

if [ ! -e /tmp/nm_eth_configured ]; then
    #set the root password to 'redhat' (for overcoming polkit easily)
    echo "Setting root password to 'redhat'"
    echo "redhat" | passwd root --stdin

    #adding ntp and syncing time
    yum -y install ntp
    service ntpd restart
    sleep 10

    #removing rate limit for systemd journaling
    sed -i 's/^#\?\(RateLimitInterval *= *\).*/\10/' /etc/systemd/journald.conf
    sed -i 's/^#\?\(RateLimitBurst *= *\).*/\10/' /etc/systemd/journald.conf
    systemctl restart systemd-journald.service

    #fake console
    echo "Faking a console session..."
    touch /run/console/test
    echo test > /run/console/console.lock

    #passwordless sudo
    echo "enabling passwordless sudo"
    if [ -e /etc/sudoers.bak ]; then
    mv -f /etc/sudoers.bak /etc/sudoers
    fi
    cp -a /etc/sudoers /etc/sudoers.bak
    grep -v requiretty /etc/sudoers.bak > /etc/sudoers
    echo 'Defaults:test !env_reset' >> /etc/sudoers
    echo 'test ALL=(ALL)   NOPASSWD: ALL' >> /etc/sudoers

    #setting ulimit to unlimited for test user
    echo "ulimit -c unlimited" >> /home/test/.bashrc

    # to prevent "Wired Connection X" mess
    # to prevent "Wired Connection X" mess
    if ! grep no-auto-default /etc/NetworkManager/NetworkManager.conf; then
        echo "no-auto-default=*" >> /etc/NetworkManager/NetworkManager.conf
        service NetworkManager restart
    fi

    #making sure all wifi devices are named wlanX
    NUM=0
    for DEV in `nmcli device | grep wifi | awk {'print $1'}`; do
    ip link set $DEV down
    ip link set $DEV name wlan$NUM
    ip link set wlan$NUM up
    NUM=$(($NUM+1))
    done

    #installing behave and pexpect
    yum -y install install/*.rpm

    veth=0
    for X in $(seq 0 10); do
        if ! nmcli -f DEVICE -t device |grep eth${X}; then
            veth=1
            break
        fi
    done


    if [ $veth -eq 1 ]; then
        NUM=0
        # renaming all possible device to parX
        for DEV in $(nmcli -f TYPE,DEVICE -t c sh -a  | grep ethernet | awk '{split($0,a,":"); print a[2]}'); do
            if [ "$DEV" == "$(ip route |grep default |awk '{print $5}')" ]; then
                ip link set $DEV down
                ip link set $DEV name par$NUM
                ip link set par$NUM up
                nmcli c add type ethernet con-name par$NUM ifname par$NUM autoconnect no
                nmcli c down par$NUM
                nmcli c del $DEV
            else
                ip link set $DEV down
            fi
        done

        # removing all possible devices
        for X in $(seq 0 10); do
            nmcli c delete id eth${X}
            ip link set dev eth${X} down
        done

        # creating eth99 device
        ip link add eth99 type veth peer name eth99p

        # adding bridge and connecting eth99 peer inside
        brctl addbr isobr
        brctl addif isobr eth99p

        # creating shared profile (dnsmasq dhcp server)
        nmcli c add type ethernet con-name eth99-srv ifname eth99
        nmcli c modify eth99-srv ipv4.method shared
        nmcli c modify eth99-srv ipv4.addresses 192.168.100.1/24

        # starting devices
        ip link set eth99 up
        ip link set eth99p up

        # starting NM profile
        nmcli c up id eth99-srv

        # creating 8 virtual devices and adding peers into bridge
        for X in $(seq 1 9); do
            ip link add eth${X} type veth peer name eth${X}p
            brctl addif isobr eth${X}p
        done

        # creating 8 NM profiles and starting them
        for X in $(seq 1 9); do
            nmcli c add type ethernet con-name eth${X} ifname eth${X} autoconnect no
            ip link set eth${X} up
            ip link set eth${X}p up
            nmcli c up id eth${X}
        done

        # creating eth0 and eth10 devices and peers
        ip link add eth0 type veth peer name eth0p
        ip link add eth10 type veth peer name eth10p

        # clonning mac address of original master device to new eth0
        ip link set dev eth0 address $(ip a s par0 |grep link/ether | awk '{print $2}')
        macaddr=$(echo $(hostname)|md5sum|sed 's/^\(..\)\(..\)\(..\)\(..\)\(..\).*$/02:\1:\2:\3:\4:\5/')
        ip link set dev par0 address $macaddr

        # adding bridge and connecting eth0 and eth10 peers inside
        brctl addbr outbr
        brctl addif outbr par0
        brctl addif outbr eth0p
        brctl addif outbr eth10p

        # creating 2 NM profiles and starting them
        nmcli c add type ethernet con-name eth0 ifname eth0 autoconnect yes
        nmcli c add type ethernet con-name eth10 ifname eth10 autoconnect no

        for X in 0 10; do
            ip link set eth${X} up
            ip link set eth${X}p up
        done
        nmcli c up id eth0

        sleep 10
        touch /tmp/nm_veth_configured

    else
        #profiles tuning
        nmcli connection modify eth0 ipv6.method ignore
        nmcli connection modify eth1 connection.autoconnect no
        nmcli connection modify eth2 connection.autoconnect no
        nmcli connection modify eth3 connection.autoconnect no
        nmcli connection modify eth4 connection.autoconnect no
        nmcli connection modify eth5 connection.autoconnect no
        nmcli connection modify eth6 connection.autoconnect no
        nmcli connection modify eth7 connection.autoconnect no
        nmcli connection modify eth8 connection.autoconnect no
        nmcli connection modify eth9 connection.autoconnect no
        nmcli connection modify eth10 connection.autoconnect no
        nmcli connection modify eth10 ipv6.method auto
        nmcli connection up id eth0
        service NetworkManager restart
    fi
    # beah-beaker-backend sanitization
    kill -9 $(ps aux|grep -v grep| grep /usr/bin/beah-beaker-backend |awk '{print $2}')
    sleep 1
    beah-beaker-backend &
    sleep 10

    touch /tmp/nm_eth_configured
fi

if [ ! -e /tmp/nm_eth_configured ]; then
    if ! nmcli con s -a |grep eth99-srv; then
        nmcli c up id eth99-srv
        sleep 2
    fi

    for X in $(seq 0 10); do
        ip link set eth${X} up
        ip link set eth${X}p up
    done

    if ! nmcli con s -a |grep eth0; then
        nmcli c up id eth0
        sleep 2
    fi
fi

# install the pyte VT102 emulator
if [ ! -e /tmp/nmtui_pyte_installed ]; then
    easy_install pip
    pip install pyte

    touch /tmp/nmtui_pyte_installed
fi

# can't have the default 'dumb' for curses to "work" even if we redirect output
# for the internal pyte based terminal
export TERM=vt102

behave nmtui/features --no-capture --no-capture-stderr -k -t $1 -f plain -o /tmp/report_$TEST.log; rc=$?

RESULT="FAIL"
if [ $rc -eq 0 ]; then
    RESULT="PASS"
fi

# only way to have screen snapshots for each step present in the individual logs
# the tui-screen log is created via environment.py
cat /tmp/tui-screen.log >> /tmp/report_$TEST.log

# this is to see the semi-useful output in the TESTOUT for failed tests too
echo "--------- /tmp/report_$TEST.log ---------"
cat /tmp/report_$TEST.log

rhts-report-result $TEST $RESULT "/tmp/report_$TEST.log"

echo "------------ Test result: $RESULT ------------"
exit $rc
