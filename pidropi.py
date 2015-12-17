import os
import configparser
from backup import *

if __name__ == '__main__':

    # Reading config
    currentDir = os.path.dirname(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read(currentDir + '/config.ini')

    # Backup mysql
    mysql = mysqlBackup(config)
    mysql.backup()

    # Backup folders
    folders = folderBackup(config)
    folders.backup()

    # Sync with Dropbox
    sync = dropboxSynchronize(config)
    sync.sync()

