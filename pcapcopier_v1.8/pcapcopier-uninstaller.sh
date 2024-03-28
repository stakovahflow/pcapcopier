#!/usr/bin/env bash
if [[ $EUID -ne 0 ]]; then
   echo "This application must be run as root (sudo)" 
   exit 1
fi
docker stop pcapcopier_v1.8
docker rm pcapcopier_v1.8
docker image rm pcapcopier_v1.8
rm -rf /opt/pcapcopier
rm -rf /home/silentdefense/.ssh/config
