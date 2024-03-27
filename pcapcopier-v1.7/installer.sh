#!/usr/bin/env bash
echo -e "Changing permissions on working directory"
chmod 755 .
echo -e "Done."

echo -e "Attempting to load pcapcopier docker image:"
docker load -i pcapcopier_v1.7.tar
echo -e "Done."

echo -e "Creating /opt/pcapcopier directory:"
mkdir -p /opt/pcapcopier
echo -e "Done."

echo -e "Copying pcapcopier-compose.yml to /opt/pcapcopier/"
cp pcapcopier-compose.yml /opt/pcapcopier/
echo -e "Done."

echo -e "Changing psermissions on /opt/pcapcopier"
chown -R silentdefense:silentdefense /opt/pcapcopier
echo -e "Done."

echo -e "Starting docker container"
echo -e "To start the PCAP copier container, run the following command:"
echo -e "    sudo docker-compose -f /opt/pcapcopier/pcapcopier-compose.yml up -d"
docker-compose -f /opt/pcapcopier/pcapcopier-compose.yml up -d
echo -e "Done."

echo -e "To log into the PCAP copier, execute the following command:"
echo -e "#####################################################################
    ssh silentdefense@127.0.0.1 -p 2022

    Container password: 4Scout123
#####################################################################
"
echo -e "To run the pcap copier appliaction, run the following command:"
echo -e "    sudo /opt/pcapcopier/bin/pcapcopier.py -h 192.168.122.121"
echo -e "    sudo /opt/pcapcopier/bin/pcapcopier.py --help"
echo -e "usage: pcapcopier.py [--help] [-l LOCATION] [-c CSV] [-h HOST] [-u USER] [-L LOCALPATH] [-R REMOTEPATH] [--timeout TIMEOUT] [--verbose]
                     [--log LOG]

Provide Customizations for Forescout eyeInspect PostgreSQL configuration

options:
  --help                show this help message and exit
  -l LOCATION, --location LOCATION
                        Location name (remote site)
  -c CSV, --csv CSV     Output CSV filename
  -h HOST, --host HOST  Remote host
  -u USER, --user USER  Remote username
  -L LOCALPATH, --localpath LOCALPATH
                        Local PCAP file directory
  -R REMOTEPATH, --remotepath REMOTEPATH
                        Remote PCAP file directory
  --timeout TIMEOUT     Timeout duration
  --verbose             Verbose output
  --log LOG             Debug log filename

"
echo -e "Installation complete
"

echo -e "To remove the docker container and associated image, run the following commands:"
echo -e "    sudo docker stop pcapcopier_v1.7"
echo -e "    sudo docker rm pcapcopier_v1.7"
echo -e "    sudo docker image rm pcapcopier_v1.7"
echo -e "    sudo rm -rf /opt/pcapcopier"
