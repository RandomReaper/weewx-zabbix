# weewx-zabbix
Allow weewx to push data to zabbix.

## Installation
## Dependencies
The `zabbix_sender` command must be available.

### Build the package:
```
mkdir -p ~/git/ && cd ~/git && git clone https://github.com/RandomReaper/weewx-zabbix.git
cd weewx-zabbix
./gen-tar.sh
```

## Install the weewx extension
sudo wee_extension --install weewx-zabbix.tgz

## Configure the weewx extension
```
# Options for extension 'zabbix'
[ZABBIX]
    # service can be disabled
    enable = true
    
    # zabbix_sender full name+path
    zabbix_sender = /usr/bin/zabbix_sender

    # Zabbix server IP
    server = 127.0.0.1

    # Zabbix host to store the values
    host = server-home
    
    # Prefix for generating the zabbix key name
    prefix = weewx_
```
## Add the key to zabbix
Add a key of type "Zabbix trapper", with the key name weewx_outTemp (formed with the prefix set in the config file + the weewx key name).

