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

Network manager: pacman -S networkmanager
systemctl enable NetworkManager

For a arch installation, the following setup needs to be done

  groupadd -r autologin
  usermod -aG autologin gustav

Setup primary display using:

  arandr

and save it using:

  autorandr --save alone

