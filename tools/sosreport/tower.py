# Copyright (c) 2015 Ansible, Inc.
# All Rights Reserved.

import sos
from distutils.version import LooseVersion

SOSREPORT_TOWER_COMMANDS = [
    "ansible --version",      # ansible core version
    "tower-manage --version", # tower version
    "supervisorctl status",   # tower process status
    "pip freeze",             # pip package list
    "tree -d /var/lib/awx",   # show me the dirs
    "ls -ll /var/lib/awx",    # check permissions
    "ls -ll /etc/tower",
    "ls -ll /var/lib/awx/job_status/"
]

SOSREPORT_TOWER_DIRS = [
    "/etc/tower/",
    "/etc/ansible/",
    "/var/log/tower",
    "/var/log/httpd",
    "/var/log/apache2",
    "/var/log/redis",
    "/var/log/supervisor",
    "/var/log/syslog",
    "/var/log/udev",
    "/var/log/kern*",
    "/var/log/dist-upgrade",
    "/var/log/installer",
    "/var/log/unattended-upgrades",
    "/var/log/apport.log"
]

SOSREPORT_FORBIDDEN_PATHS = [
    "/etc/tower/SECRET_KEY",
    "/etc/tower/tower.key",
    "/etc/tower/awx.key",
    "/etc/tower/tower.cert",
    "/etc/tower/awx.cert"
]

if LooseVersion(sos.__version__) >= LooseVersion('3.0'):
    from sos.plugins import Plugin, RedHatPlugin, UbuntuPlugin

    class tower(Plugin, RedHatPlugin, UbuntuPlugin):
        '''Collect Ansible Tower related information'''
        plugin_name = "tower"

        def setup(self):

            for path in SOSREPORT_TOWER_DIRS:
                self.add_copy_spec(path)

            for path in SOSREPORT_FORBIDDEN_PATHS:
                self.add_forbidden_path(path)

            for command in SOSREPORT_TOWER_COMMANDS:
                self.add_cmd_output(command)

else:
    import sos.plugintools

    class tower(sos.plugintools.PluginBase):
        '''Collect Ansible Tower related information'''

        def setup(self):

            for path in SOSREPORT_TOWER_DIRS:
                self.addCopySpec(path)

            for path in SOSREPORT_FORBIDDEN_PATHS:
                self.addForbiddenPath(path)

            for command in SOSREPORT_TOWER_COMMANDS:
                self.collectExtOutput(command)

