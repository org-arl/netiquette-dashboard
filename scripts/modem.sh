#!/bin/sh

cd /home/ubuntu/netiquette-dashboard

ls -1rt /mnt/logs/log*.txt | sed 's/^/cat /' | sh > /tmp/modem.txt
cat /tmp/modem.txt | python scripts/modem_temperature.py
rm -f /tmp/modem.txt

git add data/*
git commit -m "Data updated"
git push
