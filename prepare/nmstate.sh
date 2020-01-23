#! /bin/bash

yum -y install python3-devel rpm-build
rm -rf /usr/bin/python && ln -s /usr/bin/python3 /usr/bin/python
git clone https://github.com/nmstate/nmstate
cd nmstate
git checkout $(git tag |tail -1)
sh packaging/make_rpm.sh
rm -rf nmstate-*.src.rpm
yum -y install python3-libnmstate* nmstate-* 
python -m pip install pytest
