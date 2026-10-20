#!/usr/bin/python3
""" serving a website using Fabric """
from datetime import datetime
from fabric.api import local, env, run, put, sudo
import os


env.hosts = ["100.25.130.63", "100.25.200.147"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/web01"


def do_pack():
    """ pack the web static """
    local("mkdir -p versions")
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    arcf = "versions/web_static_{}.tgz".format(time)
    local("tar -cvzf {} web_static".format(arcf))

    return arcf


def do_deploy(archive_path):
    """ deploy the web static succesfully """
    if os.path.exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
