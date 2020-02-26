#!/bin/bash

set -e
set +h

iso=$(ls /var/cache/alps/binaries/*iso)
tmpdir=$(mktemp -d)
mount $iso $tmpdir
workdir=$(mktemp -d)
unsquashfs -f -d $workdir $tmpdir/aryalinux/root.sfs
umount $tmpdir

unwanted_files="adjtime
cron.daily
fstab
group
group-
gshadow
gshadow-
hostname
hosts
init.d
ld.so.cache
ld.so.conf
lfs-release
machine-id
passwd
passwd-
shadow
shadow-
sudoers
sudoers.d
sudoers.dist
"

# Cleanup
sudo systemctl enable lightdm
sudo rm -fv /etc/systemd/system/getty@tty1.service.d/override.conf
sed -i 's@sudo /var/lib/alpsui/updater.sh@@g' /home/$USER/.bashrc