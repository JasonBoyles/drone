# coding=utf8

import re

from fabric.api import env, hide, run, cd, get, task
from envassert import detect, file, package, port, process, service

artifact_files = [ 'cfn-userdata.log',
                   'heat-script.log' ]


def drone_is_responding():
    with hide('running', 'stdout'):
        site = "https://localhost/"
        homepage = run("wget --quiet --output-document - --no-check-certificate %s" % site)
        if re.search('Brad Rydzewski', homepage):
            return True
        else:
            return False


@task
def check():
    env.platform_family = detect.detect()

    assert package.installed("drone"), "Package drone is missing."
    assert file.exists("/etc/drone/drone.toml"), "/etc/drone/drone.toml is missing."
    assert file.exists("/etc/drone/ssl/drone.crt"), "SSL certificate missing."
    assert file.exists("/etc/drone/ssl/drone.key"), "SSL key missing."
    assert port.is_listening(443), "Port 443 is not listening."
    assert process.is_up("droned"), "The droned process is not running."
    assert service.is_enabled("drone"), "The drone service is not enabled."
    assert drone_is_responding(), "Drone is not responding."

@task
def collect_artifacts():
  with cd("/root"):
    for file in artifact_files:
      get(file, 'test/artifacts')
