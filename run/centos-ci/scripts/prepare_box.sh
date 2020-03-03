#! /bin/bash

sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
sudo yum config-manager --set-enabled PowerTools
curl https://copr.fedorainfracloud.org/coprs/nmstate/nm-build-deps/repo/epel-8/nmstate-nm-build-deps-epel-8.repo > /etc/yum.repos.d/nmstate-nm-build-deps-epel-8.repo


BRANCH="${1:-nm-1-22}"
CI_REPO="https://github.com/NetworkManager/NetworkManager-ci"
yum -y install git

git clone $CI_REPO

cd NetworkManager-ci

sh run/centos-ci/scripts/build.sh $BRANCH
