[[ -f ~/.Xresources ]] && xrdb -merge -I$HOME ~/.Xresources

# fix escape and capslock
xmodmap -e "clear lock" #disable caps lock switch
xmodmap -e "keysym Caps_Lock = Escape" #set caps_lock as escape

exec i3
