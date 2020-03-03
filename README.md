Theese are my dotfiles, enjoy

To add the git files use:

  git config --global include.path ~/path/to/dotfiles/_gitconfig

# Arch specific

1. Download arch iso
2. lsblk to find usb dongle
3. run dd if=arch.iso of=/dev/sdX status="progress"
4. boot from usb, read arch installation wiki

For a arch installation, the following setup needs to be done

  groupadd -r autologin
  usermod -aG autologin gustav

Setup primary display using:

  arandr

and save it using:

  autorandr --save alone

