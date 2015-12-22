from subprocess import call
from backup import Backup


class Folder(Backup):

    folders = []
    tmpPostfix = 'folders'

    def __init__(self, config):

        super(Folder, self).__init__(config)

        if 'folders' not in config or 'folders' not in config['folders']:
            raise ValueError('No folders in config, nothing to work with')

        # Set folders list
        self.set_folders(config['folders']['folders'])

    def set_folders(self, folders):
        self.folders = [x.strip() for x in folders.split(',')]
        if len(self.folders) == 0:
            raise ValueError('No folders in config')

    def backup(self):
        """
        Make backup and clean up
        """
        self.dump_folders()

        # Archive
        # super(Folder, self).archive()
        self.archive()

        # Clean up old folders
        self.cleanup_sub_folders()

    def dump_folders(self):
        # folder_name = super(Folder, self).create_current_folder_by_time()
        folder_name = self.create_current_folder_by_time()
        for folder in self.folders:
            call(['rsync', '-ar',
                  '/' + folder.strip('/'),
                  self.tmpFolder + '/' + folder_name + '/'
                  ])
