#!/usr/bin/env bash
# This does not work yet.

xautolock \
-detectsleep \
-time 30 \
-locker "python /home/slug/Projector/pS.py OFF" \
-notify 60 \
-notifier "notify-send \"Projector Bulb\" \"Projector will turn off in 60 seconds.\""
