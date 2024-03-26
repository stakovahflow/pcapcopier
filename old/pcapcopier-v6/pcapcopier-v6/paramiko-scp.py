#!/usr/bin/env python3
import paramiko
import getpass
class SFTP_Connection:
    def __init__(self):
        self.HOST = '10.66.67.11'
        self.USERNAME = 'silentdefense'
        self.PASSWORD = '4Scout123'
    def connect(self):
        try:
            self.PASSWORD = getpass.getpass()
        except Exception as exception:
            print('Exception:',exception)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(hostname = self.HOST, username = self.USERNAME, password = self.PASSWORD)
        sftp = client.open_sftp()
        print(sftp)
        dirlist = sftp.listdir('.')
        print("Directory list:",dirlist)
        sftp.chdir('/etc/')
        sftp.get('hosts','{self.HOST}')
        sftp.close()
        client.close()
if __name__ == '__main__':
    ssh = SFTP_Connection()
    ssh.connect()

