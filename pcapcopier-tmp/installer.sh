#!/usr/bin/bash

version='2024-03-17-b'

DATED=$(date +%Y%m%d-%H%M%S)

python3 ./pipinstaller.py

cp ./pcapcopier.py /usr/local/sbin/pcapcopier
chmod a+x /usr/local/sbin/pcapcopier
ls -alh /usr/local/sbin/pcapcopier

cp /tmp/pcapcopier/pcapcopier.py /usr/local/sbin/pcapcopier
exit 0
