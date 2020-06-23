#!/bin/bash
function setup () {
    MAJOR="$(uname -r |awk -F '-' '{print $1}')"
    MINOR="$(uname -r |awk -F '-' '{print $2}'|awk -F '.' '{print  $1"."$2}')"
    URL="http://download.eng.bos.redhat.com/brewroot/vol/rhel-8/packages/kernel"
    yum -y install wget git kernel-headers kernel-devel gcc

    rpm -i $URL/$MAJOR/$MINOR/src/kernel-$MAJOR-$MINOR.src.rpm

    LINUX=linux-$MAJOR-$MINOR
    PATCH=0001-netdevsim-add-mock-support-for-coalescing-and-ring-o-1.patch
    tar xf /root/rpmbuild/SOURCES/$LINUX.tar.xz -C /tmp

    cp tmp/$PATCH /tmp/$LINUX
    pushd /tmp/$LINUX
        patch -p1 < $PATCH
        cd drivers/net/netdevsim
        make -C /lib/modules/(uname -r)/build M=$PWD
        insmod netdevsim.ko
        touch /tmp/netdevsim.txt
    popd

}

function teardown () {
    modprobe -r netdevsim
    rm -rf /tmp/netdevsim.txt
}
if [ "x$1" != "xteardown" ]; then
    setup
else
    teardown
fi
