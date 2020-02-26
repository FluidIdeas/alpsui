#!/bin/bash

set -e
set +h

url="$1"

sudo mkdir -pv /var/cache/alps/binaries
pushd /var/cache/alps/binaries
sudo wget -c $url

sudo systemctl disable lightdm
sudo mkdir -pv /etc/systemd/system/getty@tty1.service.d/
pushd /etc/systemd/system/getty@tty1.service.d/
sudo tee override.conf << EOF
[Service]
Type=simple
ExecStart=
ExecStart=-/sbin/agetty --autologin $USER --noclear %I 38400 linux
EOF

echo "sudo /var/lib/alpsui/updater.sh" >> /home/$USER/.bashrc

# sudo rm -fv /etc/systemd/system/getty@tty1.service.d/override.conf

echo 'Updates downloaded. Please restart, login and run "sudo update" to install updates.'