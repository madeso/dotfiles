#!/bin/sh
mount -t cifs //NAS2/Multimedia /home/gustav/nas -o credentials=/etc/samba/credentials/nas2,workgroup=NAS,iocharset=utf8,uid=gustav,vers=1.0
