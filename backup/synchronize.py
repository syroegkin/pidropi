import dropbox
import os
from dropbox.exceptions import AuthError, ApiError

from dropbox.files import FolderMetadata
from path import path


class Synchronize:

    dbx = None
    tmpFolder = None

    def __init__(self, config):
        # Check for an access token
        if 'dropbox' not in config:
            raise ValueError('ERROR: [dropbox] section is required')
        if 'token' not in config['dropbox']:
            raise ValueError('ERROR: [dropbox][token] section is required')

        self.dbx = dropbox.Dropbox(config['dropbox']['token'])
        try:
            self.dbx.users_get_current_account()
        except AuthError:
            raise ValueError("ERROR: Invalid access token; try re-generating an access token "
                             "from the app console on the web.")
        self.tmpFolder = config['tmp']['tmpFolder']

    def sync(self):
        # Upload files to dropbox
        os.chdir(self.tmpFolder)
        directory = path('.')
        for file in directory.walk():
            if file.isfile():
                try:
                    self.dbx.files_get_metadata('/' + file[2:])
                except ApiError:
                    with open(file, 'rb') as f:
                        data = f.read()
                    self.dbx.files_upload(data, '/' + file[2:], dropbox.files.WriteMode.overwrite)
