import os
import argparse
import configparser
from backup import *


def usage():
    pass

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Backup. If no parameters are provided, '
                                                 'backup will try to use config.ini file from the current directory')
    parser.add_argument('-c', action='store', dest='config', help='path to the alternative config file')
    args = parser.parse_args()

    if args.config is None:
        # Read default config
        filename = os.path.dirname(os.path.abspath(__file__)) + '/config.ini'
    else:
        filename = args.config

    if os.path.isfile(filename) is None:
        raise ValueError("File does not exists")

    config = configparser.ConfigParser()
    config.read(filename)

    # Backup mysql
    mysql = mysqlBackup(config)
    mysql.backup()

    # Backup folders
    folders = folderBackup(config)
    folders.backup()

    # Sync with Dropbox
    sync = dropboxSynchronize(config)
    sync.sync()

