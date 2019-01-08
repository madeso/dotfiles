#!/bin/sh

# inspired by https://www.reddit.com/r/i3wm/comments/7ak40z/how_do_you_shutdown_from_i3/

i3-msg [class="."] kill && sleep 3  && systemctl poweroff -i
