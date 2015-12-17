from path import path
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

    def __init__(self, config):
        """
        Set up number of sub folders
        :param config: Configuration
        """
        if 'tmp' not in config or 'subFolders' not in config['tmp']:
            self.subFoldersNum = 3
        else:
            self.subFoldersNum = int(config['tmp']['subFolders'])

        self.set_tmp_folder(config['tmp']['tmpFolder'])

    def set_tmp_folder(self, folder):
        if folder[0] != "/":
            # Got a local folder instead
            self.tmpFolder = '../' + folder
        else:
            self.tmpFolder = folder

        if len(self.tmpPostfix) > 0:
            self.tmpFolder += '/' + self.tmpPostfix

        # Create tmp folder if it isn't here
        if not os.path.isdir(self.tmpFolder):
            os.makedirs(self.tmpFolder)
            os.chmod(self.tmpFolder, 0o777)

    def create_current_folder_by_time(self):
        """
        Creates folder in current temporary folder with a timestamp as a name
        :return: folder_name
        """
        folder_name = time.strftime("%Y%m%d%H%M%S")
        os.mkdir(self.tmpFolder + '/' + folder_name)
        return folder_name

    def archive(self):
        directories = path(self.tmpFolder)
        for directory in directories.dirs():
            call(['tar',
                  '-czf',
                  directory + '.tar.gz',
                  '-C', directory,
                  './'])
            rmtree(directory)
            # call(['gzip', '-9', directory + '.tar'])

    def cleanup_sub_folders(self):
        """
        Clean up folders in backup directory
         keep up to 3 if not defined inb config
        """
        directory = path(self.tmpFolder)
        num_files = len(directory.files())
        if num_files > self.subFoldersNum:
            files_list = []
            for file in directory.walk():
                files_list.append(file)
            files_list.sort(reverse=True)
            while len(files_list) > self.subFoldersNum:
                os.remove(files_list.pop())


