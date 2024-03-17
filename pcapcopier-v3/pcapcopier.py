#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  eyefilecopy.py
#  modified: 2024-03-16
#

version='2024-03-17-f'

import paramiko
import os
from sys import argv
import csv
from time import sleep
from getpass import getpass
from paramiko import Transport
from scp import SCPClient
from datetime import datetime
import hashlib
import logging
import argparse

application_name = argv[0]

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


def send_sudo_password(ssh, password, command):
    logging.debug(f"Invoking SSH Shell")
    channel = ssh.invoke_shell()
    sleep(1)
    logging.debug(f"Running command: {command}")
    channel.send(f"{command}\n")
    sleep(1)
    channel.send(f"{password}\n")
    sleep(1)
    channel.recv(9999)
    channel.close()

def get_file_checksum(file_path):
    # Calculate the MD5 checksum of a file
    md5 = hashlib.md5()
    logging.debug(f"Obtaining MD5 Checksum of '{file_path}'")
    with open(file_path, 'rb') as file:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file.read(4096), b""):
            md5.update(byte_block)
    logging.debug(f"MD5 Checksum for {file_path}: {md5.hexdigest()}")
    return md5.hexdigest()

def copy_pcap_files(ssh, source_path, destination_path, max_attempts=3, verbose=True):
    logging.debug(f"Copy PCAP files function received: {source_path}, {destination_path}, {max_attempts}, {verbose}, {csv_file}")
    logging.debug(f"Attempting to validate existence of PCAP files in: {source_path}")
    pcap_files_command = f"ls {source_path}/*.pcap"
    pcap_files = run_remote_command(ssh, pcap_files_command)[0].split()
    for pcap_file in pcap_files:
        logging.debug(f'PCAP found: {pcap_file}')
    all_files_transferred = True
    logging.debug(f'Attempting to create CSV file: {csv_file}')
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['Timestamp', 'Remote_Hostname', 'Remote_File', 'Local_File', 'Remote_Checksum', 'Local_Checksum', 'Transfer_Status']
        logging.debug(f'CSV Fields: {fieldnames}')
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for pcap_file in pcap_files:
            logging.debug(f'Attempting to retrieve {pcap_file} from {remote_host}')
            # Extract filename from the full path on the remote server
            remote_filename = os.path.basename(pcap_file)

            # Get hostname, remote directory, and local directory for each file
            remote_hostname = run_remote_command(ssh, "hostname")[0]
            remote_file_path = f"{source_path}/{remote_filename}"

            # Attempt the transfer up to max_attempts times
            for attempt in range(1, max_attempts + 1):
                try:
                    logging.debug(f"Attempt {attempt} of SCP file transfer: {remote_file_path}")
                    with SCPClient(ssh.get_transport()) as scp:
                        scp.get(remote_path=remote_file_path, local_path=destination_path)

                    logging.info(f"File {remote_filename} copied successfully.")
                    transfer_status = "Success"
                    break  # Break the loop if the file is copied successfully

                except Exception as e:
                    logging.error(f"Error: {e}.\n Retrying... (Attempt {attempt}/{max_attempts})")
                    if attempt == max_attempts:
                        logging.error(f"Maximum attempts reached for file {remote_filename}. Skipping.")
                        all_files_transferred = False
                        transfer_status = "Failed"
                        break  # Break the loop if maximum attempts reached
                    else:
                        sleep(1)  # Wait for a short duration before retrying

            # Print debug information for each file
            logging.info(f"Remote Hostname: {remote_hostname}, Remote Dir: {source_path}, Local Dir: {destination_path}")
            logging.info(f"Source File: {remote_filename}")

            # Checksum verification and printing if verbose is True
            local_checksum = get_file_checksum(f"{destination_path}/{remote_filename}")
            remote_checksum = run_remote_command(ssh, f"md5sum {remote_file_path}")[0].split()[0]
            logging.debug(f"Local Checksum:  {local_checksum}")
            logging.debug(f"Remote Checksum: {remote_checksum}")

            if verbose:
                print(f"Local Checksum:  {local_checksum}")
                print(f"Remote Checksum: {remote_checksum}")
            
            # Compare checksums
            if local_checksum != remote_checksum:
                logging.error(f"Checksums do not match. The file {remote_filename} may not have copied successfully.")
                transfer_status = "Checksum Mismatch"
            else:
                logging.info(f"Checksums match. Deleting file {remote_filename}.")
                sudo_command = f"sudo -S rm -rf {remote_file_path}"
                send_sudo_password(ssh, remote_password, sudo_command)
                remote_file_path_exist_command = f"if [ -f {remote_file_path} ]; then echo 'exists'; else echo 'removed'; fi"
                remote_file_path_exists = run_remote_command(ssh, remote_file_path_exist_command)[0].split()[0]
                logging.info(f"Verifying removal of remote file '{remote_file_path}': {remote_file_path_exists}")

            # Log information to CSV file
            # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            timestamped = timestamper()
            logging.debug(f"Writing information to CSV: {csv_file}")
            writer.writerow({
                'Timestamp': timestamped,
                'Remote_Hostname': remote_hostname,
                'Remote_File': remote_filename,
                'Local_File': f"{destination_path}/{remote_filename}",
                'Remote_Checksum': remote_checksum,
                'Local_Checksum': local_checksum,
                'Transfer_Status': transfer_status
            })

    return all_files_transferred

def get_remote_path(host, username, password, remote_base_directory):
    logging.debug(f"Attempting to retrieve remote path: {username}@{host}:{remote_base_directory}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, password=password)
        host_key = ssh.get_transport().get_remote_server_key()
        with open(os.path.expanduser('~/.ssh/known_hosts'), 'a') as known_hosts_file:
            known_hosts_file.write(f"{host} {host_key.get_name()} {host_key.get_base64()}\n")
        logging.debug(f"Connected to {host}.")
        remote_path = run_remote_command(ssh, get_base_remote_path_command)[0]
        logging.info(f"Remote directory exists: {remote_path}")
    except Exception as e:
        logging.error(f"Unable to log into {host} using username {username} and password provided")
        print(e)
    finally:
        logging.debug(f"Closing SSH session")
        ssh.close()
        logging.debug(f"Closed session")
    return(remote_path)

def collect_remote_pcaps(host, username, password, remote_base_directory, local_directory):
    logging.debug(f"Attempting to retrieve remote path as {username}@{host}:{remote_base_directory}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password)
        host_key = ssh.get_transport().get_remote_server_key()
        with open(os.path.expanduser('~/.ssh/known_hosts'), 'a') as known_hosts_file:
            known_hosts_file.write(f"{host} {host_key.get_name()} {host_key.get_base64()}\n")

        logging.info(f"Connected to {host}.")

        remote_base_directory_exists_command = f"test -d {remote_base_directory} && echo 'yes' || echo 'no'"
        remote_base_directory_exists = run_remote_command(ssh, remote_base_directory_exists_command)[0]
        logging.info(f"Remote directory exists: {remote_base_directory_exists}")

        if remote_base_directory_exists == 'yes':
            pcap_files_exist_command = f"test -n \"$(ls {remote_base_directory}/*.pcap 2>/dev/null)\" && echo 'yes' || echo 'no'"
            pcap_files_exist = run_remote_command(ssh, pcap_files_exist_command)[0]
            logging.info(f"Remote '*.pcap' files exist: {pcap_files_exist}")

            if pcap_files_exist == 'yes':
                print("Stopping NIDS:")
                sudo_command = f"sudo -S nidstool down all"
                send_sudo_password(ssh, password, sudo_command)
                sudo_command = f"sudo -S chown {remote_username}:{remote_username} {remote_base_directory}/*.pcap"
                send_sudo_password(ssh, password, sudo_command)

                hostname_output = run_remote_command(ssh, "hostname")[0]
                logging.info(f"Remote hostname: {hostname_output}")

                # date_output = run_remote_command(ssh, "date +'%Y-%m-%d'")[0]
                target_directory = f"{local_directory}/{hostname_output}_{timestamp}"

                # Check if the local directory exists before attempting to create it
                if not os.path.exists(target_directory):
                    os.makedirs(target_directory)
                    logging.info(f"Creating local directory: {target_directory}")
                else:
                    logging.error(f"Local directory already exists: {target_directory}")

                all_files_transferred = copy_pcap_files(ssh, remote_base_directory, target_directory)

                if all_files_transferred:
                    print("Tasks completed successfully.")
                    print("Restarting NIDS:")
                    sudo_command = f"sudo -S nidstool up all"
                    send_sudo_password(ssh, password, sudo_command)
                    sleep(2)
                    print("Done!")
                else:
                    logging.error("Some files failed to transfer. Check the output for details.")
            else:
                logging.info(f"No '*.pcap' files found on {host}.")

        else:
            logging.info(f"Remote directory '{remote_base_directory}' does not exist on {host}.")
    except Exception as e:
        logging.error(f"Unable to log into {host} using username {username} and password provided")
        logging.error(e)
    finally:
        ssh.close()

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
    else:
        log_file = '/var/log/eyefilecopy.log'

    if args.location:
        initial_location = args.location
    else:
        initial_location = input('Location: ')
    location = strip_special(initial_location)
    
    if args.csv:
        csv_file = args.csv
    else:
        csv_file = f"eyefilecopy-{timestamp}-{location}.csv"

    if args.host:
        remote_host = args.host
    else:
        remote_host = input("Host address:").strip()

    if args.user:
        remote_username = args.user
    else:
        remote_username = 'silentdefense'
    remote_password = getpass(f'Password ({remote_username}): ')
    
    if args.localpath:
        local_base_dir = args.localpath
    else:
        local_base_dir = '/opt/pcaps'

    if args.remotepath:
        remote_base_dir = args.remotepath
        print(f'Remote path: {remote_base_dir}')
    else:
        remote_base_dir = '/opt/nids-docker/states/'

    if args.timeout:
        timeout = args.timeout
        print(f'Timeout: {timeout}')
    else:
        timeout = 10

    if args.verbose:
        verbosity = True
        print(f'Verbose mode on')
    
    # Call the function to set up logging at the start of your script
    setup_logging()
    continuous_capture_dir = 'pcaps/continuous_capture'
    
    # Print a warning:
    print("If performing this operation over SSH, please ensure you're running 'screen' so that the transfer operation can be backgrounded if the session is interrupted.")
    print("About to transfer PCAP files from a remote system, verify after transfer, then delete")

    # Set our global parameters:
    get_base_remote_path_command = "find /opt/nids-docker/states/ -mindepth 1 -maxdepth 1 -type d"

    # getremotefilelist = f"find {remotepath}/pcaps/continuous_capture/"
    
    print(f"Exported transfer information to file: {csv_file}")
    sleep(1)

    #######################################################################
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
