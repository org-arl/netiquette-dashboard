#!/bin/sh

cd /home/nethq/netiquette-dashboard

DF=`df -m / | tail -1 | perl -pe 's/ +/,/g' | cut -d',' -f3,4`
echo "[{\"labels\": [\"Used\",\"Free\"], \"series\": [$DF]}" > data/df.json
DF=`df -m /mnt/datastore | tail -1 | perl -pe 's/ +/,/g' | cut -d',' -f3,4`
echo "{\"labels\": [\"Used\",\"Free\"], \"series\": [$DF]}]" >> data/df.json

find ../logs -type f -name aisLog* -mtime -1 -print | sort | sed 's/^/cat /' | sh | python scripts/hq_ais.py

git add data/*
git commit -m "Data updated"
git push
