#!/usr/bin/env bash
sudo docker stop pcapcopier_v1.8
sudo docker rm pcapcopier_v1.8
sudo docker image rm pcapcopier_v1.8
sudo rm -rf /opt/pcapcopier
