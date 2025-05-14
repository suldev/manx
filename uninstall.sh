#!/bin/bash
STATUS_OK=0
STATUS_NOT_ROOT=1

if [[ $EUID > 0 ]]; then
    echo Must be root
    exit $STATUS_NOT_ROOT
fi

MANXLIB=/usr/lib/manx/
MANXBIN=/usr/bin/
MANXCFG=/etc/manx/
SYSTEMD=/etc/systemd/

systemctl stop manx.timer 2>&1 >/dev/null
systemctl stop manx.service 2>&1 >/dev/null
systemctl disable manx.timer 2>&1 >/dev/null

rm -f $SYSTEMD/system/manx.timer
rm -f $SYSTEMD/system/manx.service
rm -rf $MANXLIB
rm -f $MANXBIN/manx
rm -f $MANXBIN/manx-daemon

systemctl daemon-reload
exit $STATUS_OK