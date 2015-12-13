import os
from abc import ABCMeta


# Abstract class
class Backup(object):

    __metaclass__ = ABCMeta

    tmpFolder = None
    subFolders = None

    def __init__(self, config):
        """
        Set up number of sub folders
        :param config: Configuration
        """
        if 'tmpFolder' not in config or 'subFolders' not in config['tmpFolder']:
            self.subFolders = 3
        else:
            self.subFolders = config['tmpFolder']['subFolders']

    def set_tmp_folder(self, folder):
        """
        :param folder: tmp folder from config
        """
        if folder[0] != "/":
            # Got a local folder instead
            self.tmpFolder = '../' + folder
        else:
            self.tmpFolder = folder

        # Create tmp folder if it isn't here
        if not os.path.isdir(self.tmpFolder):
            os.makedirs(self.tmpFolder)
            os.chmod(self.tmpFolder, 0o777)

    def cleanup_sub_folders(self):
        for folder in os.walk(self.tmpFolder):
            print(folder[0])
