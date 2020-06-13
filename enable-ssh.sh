#!/bin/sh
#################################################################
#    ssh agent
#  
cp ssh-agent.service ~/.config/systemd/user/ssh-agent.service
systemctl --user enable ssh-agent.service


