#!/bin/bash
DIR=${PWD##*/} 
TARGET=weewx-zabbix.tar.gz
tar --exclude ".git" --exclude "./gen-tar.sh" --exclude "$TARGET" -cvzf weewx-zabbix.tgz $TARGET -C .. "$DIR"
