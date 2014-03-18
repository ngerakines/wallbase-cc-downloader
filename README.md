# wallbase-cc-downloader

A small python script to download top wallpapers from wallbase.cc.

This script is used to download the top safe, sketchy and nsfw wallpapers to a directory to be randomly rotated at random on my lubuntu desktop.

# Usage

Copy the wallpaper-download.sh, wallpaper-rotate.sh and download.py scripts into your bin directory.

    $ mkdir ~/tmp/
    $ git clone https://github.com/ngerakines/wallbase-cc-downloader.git
    $ cd wallbase-cc-downloader
    $ chmod +x *.sh
    $ mkdir ~/bin/
    $ cp *.sh *.py ~/bin/
    $ touch ~/.wallbase-cc-blacklist

Update the paths, username and password in the bash scripts.

Then update your crontab with the following:

    0 1 * * * /path/to/wallpaper-download.sh
    */5 * * * * export DISPLAY=:0 && /path/to/wallpaper-rotate.sh

And done. New wallpapers will be fetched once a day at 1:00 am. The desktop wallpaper will be rotated every 5 minutes.

Note: I included the top 60 NSFW wallpapers, but depending on your situation, you may want to remove it.

## Blacklist

You may come accross wallpapers that are rated highly but either aren't your style or don't look good on your desktop. Simply add the full file path to the blacklist file that is configured and it will be skipped on future downloads if you delete the file.

An example blacklist would look like

    $ cat ~/.wallbase-cc-blacklist
    /path/to/dl-wallpaper-01010101.jpg
