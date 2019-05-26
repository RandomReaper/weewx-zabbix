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

from datetime import datetime
import os

import weeutil.weeutil
import weewx.engine
import weewx.units
import weewx

from subprocess import Popen, PIPE, STDOUT

import syslog

def logmsg(dst, msg):
    syslog.syslog(dst, 'zabbix: %s' % msg)

def logdbg(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)

class Zabbix(weewx.engine.StdService):
    def __init__(self, engine, config_dict):
        super(Zabbix, self).__init__(engine, config_dict)

	loginf("init")
        conf = config_dict['ZABBIX']
        self.enable = weeutil.weeutil.to_bool(conf.get('enable', False))
        self.zabbix_sender = conf.get('zabbix_sender', '/usr/bin/zabbix_sender')
        self.prefix = conf.get('prefix', 'weewx_')
        self.server = conf.get('server', '127.0.0.1')
        self.host = conf.get('host', 'weewx-host')
        if conf.has_key('units'):
            if conf['units'] == "US":
                self.unit_system = weewx.US
            if conf['units'] == "METRIC":
                self.unit_system = weewx.METRIC
            if conf['units'] == "METRICWX":
               self.unit_system = weewx.METRICWX
        else:
            self.unit_system = None

        logdbg("self.enable=" + str(self.enable))
        logdbg("self.zabbix_sender=" + self.zabbix_sender)
        logdbg("self.prefix=" + self.prefix)
        logdbg("self.server=" + self.server)
        logdbg("self.host=" + self.host)
        logdbg("self.unit_system=" + str(self.unit_system))

        if self.enable:
	        self.bind(weewx.NEW_LOOP_PACKET, self.loop)

    def loop(self, event):
	logdbg("loop data:")
        targetUnits = self.unit_system
        if targetUnits is None:
            targetUnits = event.packet['usUnits']
        convertedPacket = weewx.units.to_std_system(event.packet, targetUnits)
        s = ""
        for key,value in convertedPacket.items():
            l=self.host + " " + self.prefix+key + " " + str(value) + "\n"
            s+=l
	    logdbg(l)

	c = [self.zabbix_sender, "-z", self.server, "-i", "-"]
	logdbg("command line : " + str(c))
	p = Popen(c, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	sender_stdout = p.communicate(input=s)[0]
	loginf(self.zabbix_sender + " result: " +sender_stdout.decode())
