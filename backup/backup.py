from path import path
from abc import ABCMeta
import os
from shutil import rmtree


# Abstract class
class Backup(object):

    __metaclass__ = ABCMeta

    tmpFolder = None
    subFoldersNum = None

    def __init__(self, config):
        """
        Set up number of sub folders
        :param config: Configuration
        """
        if 'tmpFolder' not in config or 'subFolders' not in config['tmpFolder']:
            self.subFoldersNum = 3
        else:
            self.subFoldersNum = config['tmpFolder']['subFolders']

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
        directories = path(self.tmpFolder)
        num_dirs = len(directories.dirs())
        if num_dirs >= self.subFoldersNum:
            directories_list = []
            for directory in directories.walk():
                if directory.isdir():
                    directories_list.append(directory)
            directories_list.sort(reverse=True)
            while len(directories_list) >= self.subFoldersNum:
                rmtree(directories_list.pop())


