from abc import ABCMeta
from shutil import rmtree
from subprocess import call

import os
import time


# Abstract class
class Backup(object):

    __metaclass__ = ABCMeta

    tmpFolder = None
    subFoldersNum = None
    tmpPostfix = None

    tmpFolderDefault = '/tmp/pidropi'
    subFoldersNumDefault = 3

    def __init__(self, config):
        """
        Set up number of sub folders
        :param config: Configuration
        """
        if 'tmp' not in config or 'subFolders' not in config['tmp']:
            self.subFoldersNum = self.subFoldersNumDefault
        else:
            self.subFoldersNum = int(config['tmp']['subFolders'])

        if 'tmp' not in config or 'tmpFolder' not in config['tmp']:
            self.set_tmp_folder(self.tmpFolderDefault)
        else:
            self.set_tmp_folder(config['tmp']['tmpFolder'])

    def set_tmp_folder(self, folder):
        if folder[0] != "/":
            # Got a local folder instead
            self.tmpFolder = '../' + folder
        else:
            self.tmpFolder = folder

        if self.tmpPostfix is not None and len(self.tmpPostfix) > 0:
            self.tmpFolder += '/' + self.tmpPostfix

        # Create tmp folder if it isn't here
        if not os.path.isdir(self.tmpFolder):
            os.makedirs(self.tmpFolder)
            os.chmod(self.tmpFolder, 0o777)

    def create_current_folder_by_time(self, timed=None):
        """
        Creates folder in current temporary folder with a timestamp as a name
        :param timed: provide time if we need exact
        :return: folder_name
        """
        if timed is not None:
            folder_name = time.strftime("%Y%m%d%H%M%S", timed)
        else:
            folder_name = time.strftime("%Y%m%d%H%M%S")

        os.mkdir(self.tmpFolder + '/' + folder_name)
        return folder_name

    def archive(self):
        directories = [f for f in os.listdir(self.tmpFolder) if os.path.isdir(os.path.join(self.tmpFolder, f))]
        for directory in directories:
            call(['tar',
                  '-czf',
                  self.tmpFolder + '/' + directory + '.tar.gz',
                  '-C', self.tmpFolder + '/' + directory,
                  './'])
            rmtree(self.tmpFolder + '/' + directory)

    def cleanup_sub_folders(self):
        """
        Clean up folders in backup directory
         keep up to 3 if not defined inb config
        """
        files_list = [f for f in os.listdir(self.tmpFolder)
                      if os.path.isfile(os.path.join(self.tmpFolder, f))]
        files_list.sort(reverse=True)
        while len(files_list) > self.subFoldersNum:
            os.remove(self.tmpFolder + '/' + files_list.pop())
