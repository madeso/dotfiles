[[ -f ~/.Xresources ]] && xrdb -merge -I$HOME ~/.Xresources

systemctl --user import-enviroment DISPLAY
export PATH="${PATH}:~/dev/dotfiles/scripts"

exec i3
