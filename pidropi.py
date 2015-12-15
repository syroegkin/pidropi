import sys
import dropbox
import os
import configparser
#from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
from backup import mysqlBackup

if __name__ == '__main__':

    # Reading config
    print("Getting config...")
    currentDir = os.path.dirname(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read(currentDir + '/config.ini')

    # Check for an access token
    if 'dropbox' not in config:
        sys.exit('ERROR: [dropbox] section is required')
    if 'token' not in config['dropbox']:
        sys.exit('ERROR: [dropbox][token] section is required')

    # Check for backup at all
    if 'databases' not in config and 'folders' not in config:
        sys.exit('WARNING: Nothing to backup, exit...')

    # Create an instance of a Dropbox class, which can make requests to the API.
    # print("Creating a Dropbox object...")
    # dbx = dropbox.Dropbox(config['dropbox']['token'])
    #
    # # Check that the access token is valid
    # try:
    #     dbx.users_get_current_account()
    # except AuthError as err:
    #     sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

    mysql = mysqlBackup(config)
    mysql.backup()

