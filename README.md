Theese are my dotfiles, enjoy

To add the git files use:

  git config --global include.path ~/path/to/dotfiles/_gitconfig

Enable start the ssh-agent systemd service>

  systemctl --user enable ssh-agent.service
  systemctl --user start ssh-agent.service

