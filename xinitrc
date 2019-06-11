[[ -f ~/.Xresources ]] && xrdb -merge -I$HOME ~/.Xresources

systemctl --user import-enviroment DISPLAY

exec i3
