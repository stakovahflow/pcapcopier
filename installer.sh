#!/usr/bin/env bash
version='2024-03-16-a'
DATED=$(date +%Y%m%d-%H%M%S)

pip3 install --no-index --no-deps tmp/wheels/bcrypt-4.1.2-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip3 install --no-index --no-deps tmp/wheels/PyNaCl-1.5.0-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl
pip3 install --no-index --no-deps tmp/wheels/pycparser-2.21-py2.py3-none-any.whl
pip3 install --no-index --no-deps tmp/wheels/scp-0.14.5-py2.py3-none-any.whl
pip3 install --no-index --no-deps tmp/wheels/paramiko-3.4.0-py3-none-any.whl
pip3 install --no-index --no-deps tmp/wheels/cffi-1.16.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
pip3 install --no-index --no-deps tmp/wheels/cryptography-42.0.5-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

cp ./tmp/pcapcopier.py /usr/local/sbin/pcapcopier
chmod a+x /usr/local/sbin/pcapcopier
ls -alh /usr/local/sbin/pcapcopier


cp /tmp/pcapcopier/pcapcopier.py /usr/local/sbin/pcapcopier
exit 0
