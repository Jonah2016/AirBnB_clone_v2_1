#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['142.44.167.228', '144.217.246.195']


def do_deploy(arch_path):
    """distributes an archive to the web servers"""
    if exists(arch_path) is False:
        return False
    try:
        fl_nm = arch_path.split("/")[-1]
        no_extn = fl_nm.split(".")[0]
        path = "/data/web_static/releases/"
        put(arch_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_extn))
        run('tar -xzf /tmp/{} -C {}{}/'.format(fl_nm, path, no_extn))
        run('rm /tmp/{}'.format(fl_nm))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_extn))
        run('rm -rf {}{}/web_static'.format(path, no_extn))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_extn))
        return True
    except:
        return False
