from subprocess import call
from backup import Backup


class Folder(Backup):

    folders = []
    tmpPostfix = 'folders'

    def __init__(self, config):
        super(Folder, self).__init__(config)
        if 'folders' not in config or 'folders' not in config['folders']:
            raise ValueError('No folders in config, nothing to work with')
        self.set_folders(config['folders']['folders'])

    def set_folders(self, folders):
        """
        Set folders list
        :param folders: folders string separated by comma
        """
        self.folders = [x.strip() for x in folders.split(',')]
        if len(self.folders) == 0:
            raise ValueError('No folders in config')

    def backup(self):
        """
        Make backup and clean up
        """
        self.dump_folders()
        self.archive()
        self.cleanup_sub_folders()

    def dump_folders(self):
        folder_name = self.create_current_folder_by_time()
        for folder in self.folders:
            call(['rsync', '-ar',
                  '/' + folder.strip('/'),
                  self.tmpFolder + '/' + folder_name + '/'
                  ])
