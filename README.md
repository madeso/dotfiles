Theese are my dotfiles, enjoy

To add the git files use:

  git config --global include.path ~/path/to/dotfiles/_gitconfig

# Arch specific

1. Download arch iso
2. lsblk to find usb dongle
3. run dd if=arch.iso of=/dev/sdX status="progress"
4. boot from usb, read arch installation wiki
dos="for bios", gpt="for uefi"
Boot: 200 M
Swap: 150% of (potential) ram
Root/home: 23-32 GB (currently 25 is ok)

get ram size:

  free -h --si

For a arch installation, the following setup needs to be done

  groupadd -r autologin
  usermod -aG autologin gustav

Setup primary display using:

  arandr

and save it using:

  autorandr --save alone

