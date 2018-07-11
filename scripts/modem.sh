#!/bin/sh

cd /home/ubuntu/netiquette-dashboard

ls -1rt /mnt/logs/log*.txt | sed 's/^/cat /' | sh > /tmp/modem.txt
cat /tmp/modem.txt | python scripts/modem_temperature.py
cat /tmp/modem.txt | python scripts/modem_noise.py
cat /tmp/modem.txt | python scripts/modem_comms.py
rm -f /tmp/modem.txt

DF=`df -m /mnt | tail -1 | perl -pe 's/ +/,/g' | cut -d',' -f3,4`
echo "{\"labels\": [\"Used\",\"Free\"], \"series\": [$DF]}" > data/df.json

git add data/*
git commit -m "Data updated"
git push
