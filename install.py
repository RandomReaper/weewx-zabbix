#############################################################################
#
# \brief   Post weewx data to zabbix
#
# \author  marc at pignat.org
#
# \url     https://github.com/RandomReaper/weewx-zabbix
#
#############################################################################
# 
# Copyright 2018 Marc Pignat
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# See the License for the specific language governing permissions and
# limitations under the License.
#
#############################################################################

from setup import ExtensionInstaller

def loader():
    return ZabbixInstaller()

class ZabbixInstaller(ExtensionInstaller):
    def __init__(self):
        super(ZabbixInstaller, self).__init__(
            version='0.1',
            name='zabbix',
            description='Push data to zabbix server',
            author='Marc Pignat',
            author_email='marc@pignat.org',
            process_services='user.zabbix.Zabbix',
            config={
                'ZABBIX': {
                    'enable' : 'true',
                    'zabbix_sender': '/usr/bin/zabbix_sender',
                    'prefix': 'weewx_',
                    'server': '127.0.0.1',
                    'host': 'weewx-host',
                    'units': 'US',
                },
            },
            files=[('bin/user', ['bin/user/zabbix.py'])]
        )
