#!/usr/bin/env bash
APPVERSION='2024-03-28-a'
VERSION="pcapcopier_v1.8"
if [[ $EUID -ne 0 ]]; then
   echo "This application must be run as root (sudo)" 
   exit 1
fi

# Global variables:
USERNAME="silentdefense"

# Container-based persistent variables:
PERSISTBASE="/opt/pcapcopier"
PERSISTPATH="${PERSISTBASE}/persistent/"
PERSISTLOG="${PERSISTBASE}/log"
PERSISTCSV="${PERSISTBASE}/csv"
PERSISTHOME="${PERSISTPATH}/home"
PERSISTHOMEDIR="${PERSISTPATH}/${USERNAME}"
PERSISTSSHDIR="${PERSISTHOMEDIR}/.ssh"
PERSISTAUTHKEYS="${PERSISTSSHDIR}/authorized_keys"

# Local variables:
LOCALHOMEDIR="/home/${USERNAME}"
LOCALSSHDIR="${HOMEDIR}/.ssh"
SSHPRIVATEKEY="${LOCALSSHDIR}/id_ecdsa"
SSHPUBLICKEY="${LOCALSSHDIR}/id_ecdsa.pub"
SSHCONFIG='Host 127.0.0.1
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null'
LOCALSSHCONFIG="${LOCALSSHDIR}/config"
USERID="1000"
GROUPID="1000"

# Create persistent directory structures
mkdir -p "${PERSISTHOMEDIR}"
mkdir -p "${PERSISTSSHDIR}"
mkdir -p "${PERSISTLOG}"
mkdir -p "${PERSISTCSV}"

if [ -d "$LOCALHOMEDIR" ]; then
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
  mkdir -p "$LOCALSSHDIR"
  chmod 700 "$LOCALSSHDIR"
  chown -R "$USERNAME":"$USERNAME" "$LOCALSSHDIR"
  echo -e "An ecdsa key was not found in: $LOCALSSHDIR"
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

echo -e "Creating authorized keys from $SSHPUBLICKEY: "
cat "$SSHPUBLICKEY" >> "$PERSISTAUTHKEYS"
chmod 600 "$PERSISTAUTHKEYS"
echo "$SSHCONFIG" > "$LOCALSSHCONFIG"
chown -R "$USERNAME:$USERNAME" "$LOCALSSHDIR"

echo -e "Changing permissions on working directory"
chown -R "$USERNAME:$USERNAME" .
echo -e "Done."

echo -e "Attempting to load pcapcopier docker image:"
docker load -i "$VERSION.tar"
echo -e "Done."

echo -e "Copying pcapcopier-compose.yml to $PERSISTBASE"
cp pcapcopier-compose.yml "$PERSISTBASE/"
cp pcapcopier-uninstaller.sh "$PERSISTBASE/"
chmod a+x "$PERSISTBASE/pcapcopier-uninstaller.sh"
echo -e "Done."

echo -e "Changing permissions on $PERSISTLOG"
chown -R "$USERNAME":"$USERNAME" "$PERSISTBASE"
chown -R "$USERNAME":"$USERNAME" "$PERSISTCSV"
chown -R "$USERID":"$GROUPID" "$PERSISTHOMEDIR"
echo -e "Done."

echo -e "Starting docker container"
echo -e "To start the PCAP copier container, run the following command:"
echo -e "    sudo docker-compose -f $PERSISTBASE/pcapcopier-compose.yml up -d"
docker-compose -f $PERSISTBASE/pcapcopier-compose.yml up -d
echo -e "Done."

echo -e "To log into the PCAP copier, execute the following command:"
echo -e "#####################################################################
    ssh silentdefense@127.0.0.1 -p 2022

    Container password: 4Scout123
#####################################################################
"
echo -e "To run the pcap copier application, run the following command:
    sudo $PERSISTBASE/bin/pcapcopier.py -h 192.168.123.111
    sudo $PERSISTBASE/bin/pcapcopier.py --help
    sudo $PERSISTBASE/bin/pcapcopier.py

options:
  --help                show this help message and exit
  -l LOCATION, --location LOCATION
                        Location name (remote site)
  -c CSV, --csv CSV     Output CSV filename
  -h HOST, --host HOST  Remote host
  -u USER, --user USER  Remote username
  -L PERSISTPATH, --PERSISTPATH PERSISTPATH
                        Local PCAP file directory
  -R REMOTEPATH, --remotepath REMOTEPATH
                        Remote PCAP file directory
  --timeout TIMEOUT     Timeout duration
  --verbose             Verbose output
  --log LOG             Debug log filename

"
echo -e "Installation complete"
echo -e ""
echo -e "To remove the docker container and associated image, run the following command:"
echo -e "    sudo $PERSISTBASE/pcapcopier-uninstaller.sh"
