#!/bin/bash
set -x

logger -t $0 "Running test $1"

export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin
DIR=$(pwd)


. $DIR/nmcli/gsm_hub.sh
. $DIR/prepare/envsetup.sh
setup_configure_environment "$1"

# set TEST variable for version_control script
if [ -z "$TEST" ]; then
    logger "setting test name to NetworkManager_Test0_$1"
    NMTEST="NetworkManager-ci_Test0_$1"
elif ! [ $TEST == "sanity-tests" ]; then
    NMTEST="$TEST"
fi

if [ -z "$NMTEST" ]; then
    logger "cannot set NMTEST var"
    exit 128
fi

NMTEST_REPORT=/tmp/report_$NMTEST.html


# check if we have gsm_hub use this
if [[ $1 == gsm_hub* ]];then
    # Test 3 modems on USB hub with 8 ports.
    test_modems_usb_hub; rc=$?
# if we do not have tag or gsm_hub
else
    (cd $DIR/nmcli/pytest; pytest -v -k "test_${1} and not test_${1}_" --html="$NMTEST_REPORT" .); rc=$?
fi

# check for skip
if grep -q SKIPPED "$NMTEST_REPORT" ; then
    rc=77
fi

if [ $rc -eq 0 ]; then
    RESULT="PASS"
elif [ $rc -eq 77 ]; then
    RESULT="SKIP"
    rc=0
elif [ $rc -eq 5 ]; then
    # rc 5 means test no found - so empty report
    RESULT="SKIP"
    rm "$NMTEST_REPORT"
    rc=0
else
    RESULT="FAIL"
fi

# check for empty file: -s means nonempty
if [ -s "$NMTEST_REPORT" ]; then
    rstrnt-report-result -o "$NMTEST_REPORT" $NMTEST $RESULT
else
    echo "removing empty report file"
    rm -f "$NMTEST_REPORT"
    rstrnt-report-result -o "" $NMTEST $RESULT
fi

logger -t $0 "Test $1 finished with result $RESULT: $rc"

echo "------------ Test result: $RESULT ------------"
exit $rc
