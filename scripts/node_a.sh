#!/bin/sh

cd /home/odroid/netiquette-dashboard

ls -1rt ../logs/weatherStationLog_NODE_A_* | tail -2 | sed 's/^/cat /' | sh | grep 'PYRA$' | python scripts/node_a_weather.py

DF=`df -m / | tail -1 | perl -pe 's/ +/,/g' | cut -d',' -f3,4`
echo "{\"labels\": [\"Used\",\"Free\"], \"series\": [$DF]}" > data/df.json

git add data/*
git commit -m "Data updated"
git push
