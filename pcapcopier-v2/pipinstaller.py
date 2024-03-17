#!/usr/bin/env python3
# -*- coding: utf-8 -*-
version='2024-03-17-e'
import os

try:
    import bcrypt
except ImportError:
    print('Installing bcrypt')
    os.system(f'pip3 install --no-index --no-deps ./wheels/bcrypt-4.1.2-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl')

try:
    import pynacl
except ImportError:
    print("Installing pynacl")
    os.system(f'pip3 install --no-index --no-deps ./wheels/PyNaCl-1.5.0-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl')

try:
    import pycparser
except ImportError:
    print('Installing pycparser')
    os.system(f'pip3 install --no-index --no-deps ./wheels/pycparser-2.21-py2.py3-none-any.whl')

try:
    import scp
except ImportError:
    print('Installing scp')
    os.system(f'pip3 install --no-index --no-deps ./wheels/scp-0.14.5-py2.py3-none-any.whl')

try:
    import cffi
except ImportError:
    print('Installing cffi')
    os.system(f'pip3 install --no-index --no-deps ./wheels/cffi-1.16.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl')

try:
    import cryptography
except ImportError:
    print('Installing cyptography')
    os.system(f'pip3 install --no-index --no-deps ./wheels/cryptography-42.0.5-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl')

try:
    import paramiko
except ImportError:
    print('Installing paramiko')
    os.system(f'pip3 install --no-index --no-deps ./wheels/paramiko-3.4.0-py3-none-any.whl')
