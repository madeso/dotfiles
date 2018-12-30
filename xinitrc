[[ -f ~/.Xresources ]] && xrdb -merge -I$HOME ~/.Xresources

# fix escape and capslock
xmodmap -e "clear lock" #disable caps lock switch
xmodmap -e "keysym Caps_Lock = Escape" #set caps_lock as escape

# make sure ssh-agent is started
eval $(ssh-agent)

exec i3
