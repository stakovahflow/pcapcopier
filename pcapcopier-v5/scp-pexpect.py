#!/usr/bin/env python3
import sys
import os
import pexpect
import logging
from getpass import getpass
username = sys.argv[1]
host = sys.argv[2]
filename = sys.argv[3]

password = getpass("Password: ")

child = pexpect.spawn(f'scp -o "StrictHostKeyChecking no" {filename} {username}@{host}:.')
index = child.expect (["password:", "(yes/no/[fingerprint])?", pexpect.EOF, pexpect.TIMEOUT])
if child == 0:
	print("Password")
	try:
		child.sendline(password)
	except pexpect.ExceptionPexpect:
		print('Password not accepted')
elif child == 1:
	print("Fingerprint")
elif child == 2:
	print("EOF")
else:
	print("Timeout")

print(child.before.decode())