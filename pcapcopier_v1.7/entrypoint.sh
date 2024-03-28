#!/bin/sh
hostname pcapcopier
crond -f &
ssh-keygen -A
exec /usr/sbin/sshd -D -e "$@"
