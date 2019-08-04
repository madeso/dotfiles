#!/bin/sh
#################################################################
#    General
#
# Run this file with sudo
# it will enable and setup system

# ntfs usb mounting
sudo pacman -S diskie ntfs-3g

#################################################################
#    Time synchronisation
#  
# https://wiki.archlinux.org/index.php/Systemd-timesyncd
systemctl enable systemd-timesyncd.service
timedatectl set-ntp true

