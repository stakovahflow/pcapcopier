#!/usr/bin/env bash
if [[ $EUID -ne 0 ]]; then
   echo "This application must be run as root (sudo)" 
   exit 1
fi
VERSION="pcapcopier_v1.8"
USERNAME="silentdefense"
LOCALPATH="/opt/pcapcopier/localstorage/home"
LOGPATH="/opt/pcapcopier/log"
CSVPATH="/opt/pcapcopier/csv"
CUSTOMHOMEDIR="${LOCALPATH}/${USERNAME}"
SSHDIR="${HOMEDIR}/.ssh"
SSHPRIVATEKEY="${SSHDIR}/id_ecdsa"
SSHPUBLICKEY="${SSHDIR}/id_ecdsa.pub"
AUTHKEYS="${LOCALPATH}/.ssh/authorized_keys"
TMPAUTHKEYS="/tmp/authorized_keys_${USERNAME}"
SSHCONFIG='Host 127.0.0.1
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null'
SSHCONFIGPATH="${SSHDIR}/config"

mkdir -p "$LOCALPATH"

if [ -d "$HOMEDIR" ]; then
  echo "$USERNAME home directory found"
else
  echo "$USERNAME home directory not found."
  echo "Exiting"
  exit 100
fi

# If public key exists just copy it into the silentdefense authorized_keys file
if [ -f "$SSHPRIVATEKEY" ]; then
  echo -e "Found id_ecdsa private key"
else
  mkdir -p "$SSHDIR"
  chmod 700 "$SSHDIR"
  chown -R "$USERNAME":"$USERNAME" "$SSHDIR"
  echo -e "An ecdsa key was not found in: $SSHDIR"
  echo -e "Local $USERNAME password: "
  read -s LOCALPASSWD
  echo -e ""
  echo "$LOCALPASSWD" | sudo -S -u "$USERNAME" ssh-keygen -t ecdsa -N "" -f "$SSHPRIVATEKEY"
  if [ -f "$SSHPRIVATEKEY" ]; then
    echo -e "Found id_ecdsa public key"
  else
    echo -e "Unable to create id_ecdsa key. Please run the following command and try performing the installation process again:"
    echo -e "ssh-keygen -t ecdsa -N '' -f $SSHPRIVATEKEY"
    exit 101
  fi
fi

echo -e "Attempting to copy and deduplicate authorized_keys"
cat "$SSHPUBLICKEY" >> "$AUTHKEYS"
# cat ${AUTHKEYS} | sort | uniq | grep "[a-z]" > ${TMPAUTHKEYS}; mv ${TMPAUTHKEYS} ${AUTHKEYS}
chmod 600 "$AUTHKEYS"
echo "$SSHCONFIG" > "$SSHCONFIGPATH"
chown -R silentdefense:silentdefense "$SSHDIR"

echo -e "Changing permissions on working directory"
chmod 755 .
echo -e "Done."


echo -e "Attempting to load pcapcopier docker image:"
docker load -i "$VERSION.tar"
echo -e "Done."

#echo -e "Creating /opt/pcapcopier directory:"
#mkdir -p /opt/pcapcopier
#echo -e "Done."

echo -e "Copying pcapcopier-compose.yml to /opt/pcapcopier/"
cp pcapcopier-compose.yml /opt/pcapcopier/
cp pcapcopier-uninstaller.sh /opt/pcapcopier/
chmod a+x /opt/pcapcopier/pcapcopier-uninstaller.sh
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
echo -e "To run the pcap copier application, run the following command:
    sudo /opt/pcapcopier/bin/pcapcopier.py -h 192.168.123.111
    sudo /opt/pcapcopier/bin/pcapcopier.py --help
    sudo /opt/pcapcopier/bin/pcapcopier.py

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

echo -e "To remove the docker container and associated image, run the following command:"
echo -e "    sudo /opt/pcapcopier/pcapcopier-uninstaller.sh"
