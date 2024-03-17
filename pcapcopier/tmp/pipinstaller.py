#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

try:
    import bcrypt
except ImportError:
    os.system('pip3 install --no-index --no-deps tmp/wheels/bcrypt-4.1.2-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl')

try:
    import pynacl
except ImportError:
    os.system('pip3 install --no-index --no-deps tmp/wheels/PyNaCl-1.5.0-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl')

try:
    import pycparser
except ImportError:
    os.system('pip3 install --no-index --no-deps tmp/wheels/pycparser-2.21-py2.py3-none-any.whl')

try:
    import scp
except ImportError:
    os.system('pip3 install --no-index --no-deps tmp/wheels/scp-0.14.5-py2.py3-none-any.whl')

try:
    import paramiko
except ImportError:
    os.system('pip3 install --no-index --no-deps tmp/wheels/paramiko-3.4.0-py3-none-any.whl')

try:
    import cffi
except ImportError:
    os.system('pip3 install --no-index --no-deps tmp/wheels/cffi-1.16.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl')

try:
    import cryptography
except ImportError:
    os.system('pip3 install --no-index --no-deps tmp/wheels/cryptography-42.0.5-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl')
