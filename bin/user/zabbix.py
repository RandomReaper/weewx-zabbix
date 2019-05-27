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
import time
import os

import weeutil.weeutil
import weewx.engine
import weewx.units

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
        self.send_interval = conf.get('send_interval', None)

        logdbg("self.enable=" + str(self.enable))
        logdbg("self.zabbix_sender=" + self.zabbix_sender)
        logdbg("self.prefix=" + self.prefix)
        logdbg("self.server=" + self.server)
        logdbg("self.host=" + self.host)
        logdbg("self.send_interval=" + self.send_interval)

        if self.enable:
	        self.bind(weewx.NEW_LOOP_PACKET, self.loop)

    def loop(self, event):
	logdbg("loop data:")
        if self.send_interval != None && last_time != None && time.time() - last_time < self.send_interval:
            logdbg("Ignoring packet")
            return
        last_time = time.time()
        s = ""
        for key,value in event.packet.items():
            l=self.host + " " + self.prefix+key + " " + str(value) + "\n"
            s+=l
	    logdbg(l)

	c = [self.zabbix_sender, "-z", self.server, "-i", "-"]
	logdbg("command line : " + str(c))
	p = Popen(c, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	sender_stdout = p.communicate(input=s)[0]
	loginf(self.zabbix_sender + " result: " +sender_stdout.decode())
