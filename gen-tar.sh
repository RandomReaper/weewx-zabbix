#!/bin/bash
DIR=${PWD##*/}
TARGET=weewx-zabbix.tgz
tar --exclude ".*" --exclude "./gen-tar.sh" --exclude "$TARGET" -cvzf "$TARGET" -C .. "$DIR"
