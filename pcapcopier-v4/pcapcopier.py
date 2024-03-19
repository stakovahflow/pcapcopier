#!/usr/bin/env python3
version = '2024-03-18-a'
from datetime import datetime
import pexpect
import csv
import logging
from pexpect import pxssh
from getpass import getpass
import re
import hashlib
import argparse
import os
from sys import argv
from time import sleep

application_name = argv[0]

# Set our global parameters:
continuous_capture_dir = 'pcaps/continuous_capture'
remote_base_dir = '/opt/nids-docker/states/'
log_file = '/var/log/eyefilecopy.log'
remote_username = 'silentdefense'
local_base_dir = '/opt/pcaps'

# Function to replace spaces with underscores:
def strip_special(inputstring):
    newstring = inputstring.replace(' ', '_')
    return newstring

# Configure logging
def setup_logging():
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    user_message_format = '%(message)s'

    # File Handler - for log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(log_format))
    file_handler.setLevel(logging.DEBUG)

    # Stream Handler - for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(user_message_format))
    stream_handler.setLevel(logging.INFO)

    # Get the root logger and add both handlers
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

def get_file_checksum(file_path):
    # Calculate the sha256 checksum of a file
    sha256 = hashlib.sha256()
    logging.debug(f"Obtaining sha256 Checksum of '{file_path}'")
    with open(file_path, 'rb') as file:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256.update(byte_block)
    logging.debug(f"sha256 Checksum for {file_path}: {sha256.hexdigest()}")
    return sha256.hexdigest()

def timestamper():
    output = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logging.debug(output)
    return(output)

def run_remote_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode().strip()
    errors = stderr.read().decode().strip()
    logging.debug(output)
    logging.debug(errors)
    return output, errors

def sudo_command(session, password):
    sudo_prompt = re.compile('.*[$#]')
    session.sendline('sudo -s')
    i = session.expect([sudo_prompt,'assword.*: '])
    if i==0:
        print("Password not required")
        pass
    elif i==1:
        print("Password required")
        session.sendline(password)
        sudologin = session.expect([sudo_prompt,'Unable to login with password'])
        if sudologin == 0:
            pass
        elif sudologin == 1:
            raise Exception("Incorrect password")
    else:
        raise Exception("Unexpected output")
    session.set_unique_prompt

def scp_session(username, host, password, source, destination):
    try:
        s = pxssh.pxssh()
    except Exception as e:
        logging.error(e)

def ssh_session_remote_path(username,host,password):
    try:
        get_base_remote_path_command = "find /opt/nids-docker/states/ -mindepth 1 -maxdepth 1 -type d"
        ssh = pxssh.pxssh()
        ssh.login (host, username, password)
        ssh.sendline (get_base_remote_path_command)
        ssh.prompt()
        output = ssh.before.decode()
        lines = output.splitlines()[1:]
        for line in lines:
            #if re.match(r'[a-z]', line):
            print(f"output: {line}")
            get_remote_file_list_command = f'sudo find {line}/pcaps/continuous_capture/ -type f -name "*.pcap"'
            logging.info(f"Attempting to run command: {get_remote_file_list_command}")
            ssh.sendline (get_remote_file_list_command)
            ssh.expect(f"assword for {username}:")
            ssh.send(password)
            ssh.send('\r')
            ssh.prompt()
            suboutput = ssh.before.decode()
            logging.debug(suboutput)
            sublines = suboutput.splitlines()[1:]
            for subline in sublines:
                #if re.match(r'[a-z]', subline):
                print(f"Remote path: {subline}")
                if re.match("No such file or directory", subline):
                    print(f"Directory '{subline}' does not exist")
        ssh.logout()
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(str(e))
    return()

def ssh_session(username,host,password,command):
    try:
        s = pxssh.pxssh()
        s.login (host, username, password)
        s.sendline (command)
        s.prompt()
        output = s.before.decode()
        lines = output.splitlines()[1:]
        for line in lines:
            if re.match(r'[a-z]', line):
                print(f"output: {line}")
            #print(line)
        s.logout()
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(str(e))
    return()

def copy_pcap_files(ssh, source_path, destination_path, max_attempts=3, verbose=True):
    logging.debug(f"Copy PCAP files function received: {source_path}, {destination_path}, {max_attempts}, {verbose}, {csv_file}")
    logging.debug(f"Attempting to validate existence of PCAP files in: {source_path}")
    pcap_files_command = f"ls {source_path}/*.pcap"
    pcap_files = run_remote_command(ssh, pcap_files_command)[0].split()

def get_remote_path(host, username, password, remote_base_directory):
    logging.debug(f"Attempting to retrieve remote path: {username}@{host}:{remote_base_directory}")

    
def collect_remote_pcaps(remote_host, remote_username, remote_password, full_remote_pcap_dir, local_base_dir):
    logging.debug(f'Attempting to transfer remote PCAPs from {remote_username}@{remote_host}:{full_remote_pcap_dir} to {local_base_dir}')
    scp_session(remote_username, remote_host, remote_password, full_remote_pcap_dir, local_base_dir)
    return()

#######################################################################
# Add some command line arguments for easier use:
parser = argparse.ArgumentParser(conflict_handler="resolve", description='Provide Customizations for Forescout eyeInspect PostgreSQL configuration')
parser.add_argument('-l', '--location', type=str, help='Location name (remote site)')
parser.add_argument('-c', '--csv', type=str, help='Output CSV filename')
parser.add_argument('-h', '--host', type=str, help='Remote host')
parser.add_argument('-u', '--user', type=str, help='Remote username')
parser.add_argument('-L', '--localpath', type=str, help='Local PCAP file directory')
parser.add_argument('-R', '--remotepath', type=str, help='Remote PCAP file directory')
parser.add_argument('--timeout', type=int, help='Timeout duration')
parser.add_argument('--verbose', action='store_true', help='Verbose output')
parser.add_argument('--log', type=str, help="Debug log filename")

if __name__ == "__main__":
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    
    # Ensure we're running as root user:
    if os.geteuid() != 0:
        print(f"{application_name} must be run with root (sudo) permissions")
        exit(1)
    
    # Consolidate our command line arguments:
    args=parser.parse_args()
    if args.log:
        log_file = args.log
    
    # Call the function to set up logging at the start of your script
    setup_logging()

    if args.location:
        initial_location = args.location
    else:
        initial_location = input('Location: ')
    location = strip_special(initial_location)
    
    if args.csv:
        csv_file = args.csv
    else:
        csv_file = f"{timestamp}-{location}.csv"

    if args.host:
        remote_host = args.host
    else:
        remote_host = input("Host address:").strip()

    if args.user:
        remote_username = args.user

    remote_password = getpass(f'Password ({remote_username}): ')
    
    if args.localpath:
        local_base_dir = args.localpath

    if args.remotepath:
        remote_base_dir = args.remotepath
        print(f'Remote path: {remote_base_dir}')

    if args.timeout:
        timeout = args.timeout
        print(f'Timeout: {timeout}')
    else:
        timeout = 10

    if args.verbose:
        verbosity = True
        print(f'Verbose mode on')
    
    
    # Print a warning:
    print("If performing this operation over SSH, please ensure you're running 'screen' so that the transfer operation can be backgrounded if the session is interrupted.")
    print("About to transfer PCAP files from a remote system, verify after transfer, then delete")
    
    # Print CSV Path:
    print(f"SCP file transfer information: {csv_file}")
    sleep(0.1)

    #######################################################################
    logging.info("Attempting to perform initial file path reconnaissance:")
    ssh_session_remote_path(remote_username,remote_host,remote_password)
    logging.info("Completed.")
    
    # ssh_session(username, host, password, command)
    """
    try:
        remote_base_pcap_dir = get_remote_path(remote_host, remote_username, remote_password, remote_base_dir)
        full_remote_pcap_dir = f'{remote_base_pcap_dir}/{continuous_capture_dir}'
        logging.info(f"Remote PCAP Directory: {full_remote_pcap_dir}")
        collect_remote_pcaps(remote_host, remote_username, remote_password, full_remote_pcap_dir, local_base_dir)
        logging.info(f"Completed PCAP Copy Operation {timestamper()}")
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user")
    except Exception as e:
        logging.error("An error occurred and you'll need to look through the logs")
        logging.error(e)
"""

