Add the following to fstab

credentials should contain something like:

```
username=USER
password=PASSWORD
```


```
# nas
# arch wiki says: //SERVER/sharename /mnt/mountpoint cifs username=myuser,password=mypass 0 0
# https://wiki.archlinux.org/index.php/Samba
//NAS2/Multimedia /home/gustav/nas cifs credentials=/etc/samba/credentials/nas2,workgroup=NAS,iocharset=utf8,uid=gustav,vers=1.0 0 0
```
