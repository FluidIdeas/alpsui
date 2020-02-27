#!/bin/bash

set -e
set +h

iso=$(ls /var/cache/alps/binaries/*iso)
tmpdir=$(mktemp -d)
mount $iso $tmpdir
workdir=$(mktemp -d)
unsquashfs -f -d $workdir $tmpdir/aryalinux/root.sfs
umount $tmpdir

etc_no_overwrite="adjtime
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
locale.conf
machine-id
passwd
passwd-
resolv.conf
shadow
shadow-
sudoers
sudoers.d
sudoers.dist
xdg/user-dirs.conf
xdg/user-dirs.defaults
"

root_no_overwrite="dev
home
proc
run
sys
tmp
"

for f in $(find $workdir | sed "s@$workdir/@@g"); do
    for x in $(echo $root_no_overwrite); do
        if [ "x$x" != "x$f" ]; then
            for y in $(echo $etc_no_overwrite); do
                if [ "xetc/$y" != "x$f" ]
                    sudo cp -prvf $workdir/$f /
                else
                    echo "Skipped $f"
                fi
            done
        else
            echo "Skipped dir $f"
        fi
    done
done

sudo update-desktop-database
sudo update-mime-database /usr/share/mime
sudo dracut -f /boot/initrd.img-$(ls $workdir/lib/modules) $(ls $workdir/lib/modules)
sudo grub-mkconfig -o /boot/grub/grub.cfg

# Cleanup
sudo systemctl enable lightdm
sudo rm -fv /etc/systemd/system/getty@tty1.service.d/override.conf
sed -i 's@sudo /var/lib/alpsui/updater.sh@@g' /home/$USER/.bashrc