#!/bin/sh
crond -f &
ssh-keygen -A
exec /usr/sbin/sshd -D -e "$@"
