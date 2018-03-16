#!/bin/bash
DIR=${PWD##*/}
TARGET=weewx-zabbix.tgz
rm -rf $TARGET
tar --exclude ".*" --exclude "./gen-tar.sh" -cvzf "../$TARGET" -C .. "$DIR"
mv "../$TARGET" .
