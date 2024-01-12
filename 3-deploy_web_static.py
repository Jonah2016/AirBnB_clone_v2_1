#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['142.44.167.228', '144.217.246.195']


def do_pack():
    """generates a tgz archive"""
    try:
        dt = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        fl_name = "versions/web_static_{}.tgz".format(dt)
        local("tar -cvzf {} web_static".format(fl_name))
        return fl_name
    except:
        return None


def do_deploy(arch_path):
    """distributes an archive to the web servers"""
    if exists(arch_path) is False:
        return False
    try:
        file_nm = arch_path.split("/")[-1]
        no_ext = file_nm.split(".")[0]
        path = "/data/web_static/releases/"
        put(arch_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_nm, path, no_ext))
        run('rm /tmp/{}'.format(file_nm))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    arch_path = do_pack()
    if arch_path is None:
        return False
    return do_deploy(arch_path)
