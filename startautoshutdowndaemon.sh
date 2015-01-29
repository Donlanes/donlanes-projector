#!/usr/bin/env bash
# This does not work yet.
# When it does, please change -time to 30 minutes.

xautolock \
-detectsleep \
-time 1 \
-locker "python /home/slug/Projector/projector.py OFF" \
-notify 60 \
-notifier "notify-send \"Projector Bulb\" \"Projector will turn off in 60 seconds.\""
