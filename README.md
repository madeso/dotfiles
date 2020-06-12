Theese are my dotfiles, enjoy

To add the git files use:

  git config --global include.path ~/path/to/dotfiles/_gitconfig

# Arch specific

1. Download arch iso
2. lsblk to find usb dongle
3. run dd if=arch.iso of=/dev/sdX status="progress"
4. boot from usb, read arch installation wiki

dos="for bios", gpt="for uefi"

Boot: 200 M (bootable)
Swap: 150% of (potential) ram (type 82/swap)
Root/home: 23-32 GB (currently 25 is ok for root)

get ram size:

  free -h --si

fdisk quick

fdisk /dev/sdX

(M)anual
(P)rint
(N)ew partion, last sector = "size": +200M (megabyte) +12G (gigabyte)
(D)elete partion

locale: set swedish locale but english language

Network manager: pacman -S networkmanager
systemctl enable NetworkManager

when installing, remember to install vim, sudo, which, unzip


    as root:
    useradd -m -g wheel gustav
    passwd gustav
    add to /etc/sudoers using visudo

    logout and login
    download dotfiles via git http and init submodules
    run install scripts in order
    
    to add autologin:
    groupadd -r autologin
    usermod -aG autologin gustav

    /etc/lightdm/lightdm.conf
    [Seat:*]
    autologin-user=gustav

Setup primary display using:

    arandr

and save it using:

    autorandr --save alone

in thunderbird add the followin calender for swedish holidays

    https://calendar.google.com/calendar/ical/en.swedish%23holiday%40group.v.calendar.google.com/public/basic.ics
