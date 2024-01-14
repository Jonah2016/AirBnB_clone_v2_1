#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.
import os.path
from fabric import task, Connection, Config

env = {"hosts": ["54.165.43.217", "34.229.70.47"]}

@task
def do_deploy(ctx, archive_path):
    """Distributes an archive to a web server.
    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Create a Connection object
    conn = Connection(ctx["host"])

    # Use the Connection object to run commands
    result = conn.put(archive_path, "/tmp/{}".format(file))
    if result.failed:
        return False

    result = conn.run("rm -rf /data/web_static/releases/{}/".format(name))
    if result.failed:
        return False

    result = conn.run("mkdir -p /data/web_static/releases/{}/".format(name))
    if result.failed:
        return False

    result = conn.run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name))
    if result.failed:
        return False

    result = conn.run("rm /tmp/{}".format(file))
    if result.failed:
        return False

    result = conn.run("mv /data/web_static/releases/{}/web_static/* "
                      "/data/web_static/releases/{}/".format(name, name))
    if result.failed:
        return False

    result = conn.run("rm -rf /data/web_static/releases/{}/web_static".format(name))
    if result.failed:
        return False

    result = conn.run("rm -rf /data/web_static/current")
    if result.failed:
        return False

    result = conn.run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))
    if result.failed:
        return False

    return True

