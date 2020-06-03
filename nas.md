Add the following to fstab

create nas directory in home if it's missing

```
# nas
# arch wiki says: //SERVER/sharename /mnt/mountpoint cifs username=myuser,password=mypass 0 0
# https://wiki.archlinux.org/index.php/Samba
//NAS2/Multimedia /home/gustav/nas cifs credentials=/etc/samba/credentials/nas2,workgroup=NAS,iocharset=utf8,uid=gustav,vers=1.0 0 0
```

create credentials directory if it's missing

the credentials file should contain something like:

```
username=USER
password=PASSWORD
```

