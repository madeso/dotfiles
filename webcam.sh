#!/bin/sh
vlc v4l2:// :input-slave=alsa:// :v4l-vdev="/dev/video0"

