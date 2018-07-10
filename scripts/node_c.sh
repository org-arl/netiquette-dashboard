#!/bin/sh

cd /home/odroid/netiquette-dashboard

ls -1rt ../logs/chargerLog_NODE_C_* | tail -2 | sed 's/^/cat /' | sh | python scripts/node_c_pv.py

git add data/*
git commit -m "Data updated"
git push
