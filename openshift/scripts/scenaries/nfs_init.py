#   TODO: add mounst logic 
NFS_CONF_STR="/var/ftp/pub                   192.168.54.0/255.255.255.0(ro,sync,no_wdelay,no_subtree_check,nohide)"
init_nfs = ["sudo -c 'systemctl enable rpcbind'", "sudo -c 'systemctl enable nfs-server'", "sudo -c 'service rpcbind start'", "sudo -c 'service nfs-server start'", "sudo systemctl restart nfs-server.service", "sudo restorecon /etc/exports", "sudo service nfsd restart", "mkdir /media/nfs"]


if __name__ == "__main__":
    with open("/etc/exports", "w") as f:
        f.write(NFS_CONF_STR)
