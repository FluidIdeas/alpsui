#!/bin/bash

set -e
set +h

sudo cp -v alpsui.py /usr/bin
sudo chmod -v a+x /usr/bin/alpsui.py

sudo mkdir -pv /var/lib/alpsui/

sudo cp -v  api.py \
            category_list.py \
            filters.py \
            functions.py \
            installerthread.py \
            menubar.py \
            packagelist.py \
            searchbar.py \
            shellwindow.py \
            statusbar.py \
            streamtextbuffer.py \
            toolbar.py \
            updaterthread.py \
            updater.sh \
            update-downloader.sh \
            /var/lib/alpsui/

sudo chmod a+x /var/lib/alpsui/*.sh

sudo cp -v alpsui.desktop /usr/share/applications/
sudo update-desktop-database

echo "Installation successful."