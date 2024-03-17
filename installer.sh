#!/usr/bin/env bash
version='2024-03-16-a'

ls -lh /tmp/pcapcopier/wheels/PyNaCl-1.5.0.whl
ls -lh /tmp/pcapcopier/wheels/bcrypt-4.1.2.whl
ls -lh /tmp/pcapcopier/wheels/cffi-1.16.0.whl
ls -lh /tmp/pcapcopier/wheels/cryptography-42.0.5.whl
ls -lh /tmp/pcapcopier/wheels/paramiko-3.4.0.whl
ls -lh /tmp/pcapcopier/wheels/pycparser-2.21.whl
ls -lh /tmp/pcapcopier/wheels/scp-0.14.5.whl

#pip3 install /tmp/pcapcopier/wheels/PyNaCl-1.5.0.whl
#pip3 install /tmp/pcapcopier/wheels/bcrypt-4.1.2.whl
#pip3 install /tmp/pcapcopier/wheels/cffi-1.16.0.whl
#pip3 install /tmp/pcapcopier/wheels/cryptography-42.0.5.whl
#pip3 install /tmp/pcapcopier/wheels/paramiko-3.4.0.whl
#pip3 install /tmp/pcapcopier/wheels/pycparser-2.21.whl
#pip3 install /tmp/pcapcopier/wheels/scp-0.14.5.whl

cp /tmp/pcapcopier/pcapcopier.py /usr/local/sbin/pcapcopier
exit 0
