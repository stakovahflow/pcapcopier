#!/usr/bin/env bash
IMAGENAME="pcapcopier_v1.8"
sudo docker stop $IMAGENAME
sudo docker rm $IMAGENAME
sudo docker image rm $IMAGENAME
sudo rm -rf /opt/pcapcopier
sudo docker build -t $IMAGENAME .
docker image save -o $IMAGENAME/$IMAGENAME.tar $IMAGENAME:latest
makeself $IMAGENAME/ pcapcopier-installer-v1.8.run "PCAP copier" ./installer.sh
echo -e ""
echo -e "Docker Images:"
docker images
echo -e ""
echo -e "Docker PS:"
docker ps
