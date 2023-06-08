#!/usr/bin/env sh
mkdir -p /state/dbs

trap 'pkill -P $$; exit 0' EXIT INT TERM

python3 simulator.py /state https://uniiiu.mooo.com &

# Reap orphans
wait
