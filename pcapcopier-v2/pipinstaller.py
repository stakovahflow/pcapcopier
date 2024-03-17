#!/usr/bin/env python3
# -*- coding: utf-8 -*-
version='2024-03-17-e'
import os

package = "./wheels/bcrypt-4.1.2-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
try:
    import bcrypt
except ImportError:
    print('Installing bcrypt')
    os.system(f'pip3 install --no-index --no-deps {package}')
except Exception as e:
    print(f'Unable to either import or install pip package {package}')

package = "./wheels/PyNaCl-1.5.0-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_24_x86_64.whl"
try:
    import pynacl
except ImportError:
    os.system(f'pip3 install --no-index --no-deps {package}')
except Exception as e:
    print(f'Unable to either import or install pip package {package}')


package = "./wheels/pycparser-2.21-py2.py3-none-any.whl"
try:
    import pycparser
except ImportError:
    os.system(f'pip3 install --no-index --no-deps {package}')
except Exception as e:
    print(f'Unable to either import or install pip package {package}')

package = "./wheels/scp-0.14.5-py2.py3-none-any.whl"
try:
    import scp
except ImportError:
    os.system(f'pip3 install --no-index --no-deps {package}')
except Exception as e:
    print(f'Unable to either import or install pip package {package}')

package = "./wheels/cffi-1.16.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
try:
    import cffi
except ImportError:
    os.system(f'pip3 install --no-index --no-deps {package}')
except Exception as e:
    print(f'Unable to either import or install pip package {package}')

package = "./wheels/cryptography-42.0.5-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl"
try:
    import cryptography
except ImportError:
    os.system(f'pip3 install --no-index --no-deps {package}')
except Exception as e:
    print(f'Unable to either import or install pip package {package}')

package = "./wheels/paramiko-3.4.0-py3-none-any.whl"
try:
    import paramiko
except ImportError:
    os.system(f'pip3 install --no-index --no-deps {package}')
except Exception as e:
    print(f'Unable to either import or install pip package {package}')
