#!/bin/sh

DISABLE_FILE="/path/to/.wallpaper-rotate-disable"
LOG_FILE=/path/to/.wallpaper-rotate.log

if [ -f "$DISABLE_FILE" ]
then
    exit
fi


WALLPAPER=$(find /path/to/your/wallpapers/ -name *jpg -type f | shuf -n1)
pcmanfm --set-wallpaper="$WALLPAPER"

echo "$(date) $WALLPAPER" >> $LOG_FILE
