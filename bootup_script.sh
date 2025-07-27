#!/bin/bash
LOCKFILE=/tmp/main_py.lock

(
    flock -n 200 || { echo "Script already running."; exit 1;}
    source ~/Projects/ghost_gear/.venv/bin/activate
    python ~/Projects/ghost_gear/main.py
) 200>$LOCKFILE