#!/bin/sh
pcmanfm --set-wallpaper="$(find /path/to/your/wallpapers/ -name *jpg -type f | shuf -n1)"
