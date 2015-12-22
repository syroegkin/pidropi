import mock
import copy
import unittest

from backup.folder import Folder
from fixtures import config


class TestFolder(unittest.TestCase):

    def test_init_with_wrong_config(self):
        config_changed = copy.deepcopy(config)
        del config_changed['folders']
        with self.assertRaises(ValueError):
            folder = Folder(config_changed)

    @mock.patch.object(Folder, 'set_folders')
    def test_init_single_folder(self, mock_set_folders):
        folder = Folder(config)
        self.assertTrue(mock_set_folders.called)

    def test_set_folders_single_folder(self):
        folder = Folder(config)
        folders = '/tmp/pmt'
        folder.set_folders(folders)
        self.assertEqual(folder.folders, [folders])

    def test_set_folders_multiple_folders(self):
        folder = Folder(config)
        two_folders = '/tmp/1,/tmp/2'
        folder.set_folders(two_folders)
        self.assertEqual(folder.folders,
                         [x.strip() for x in two_folders.split(',')])

        more_folders = '/tmp/1, /tmp/2,/tmp/3,    /tmp/4'
        folder.set_folders(more_folders)
        self.assertEqual(folder.folders,
                         [x.strip() for x in more_folders.split(',')])

    @mock.patch('backup.folder.call')
    @mock.patch.object(Folder, 'create_current_folder_by_time')
    def test_dump_folders(self, mock_create, mock_call):
        folder = Folder(config)
        folder.dump_folders()
        self.assertTrue(mock_create.called)
        self.assertTrue(mock_call.called)

    @mock.patch.object(Folder, 'dump_folders')
    @mock.patch.object(Folder, 'archive')
    @mock.patch.object(Folder, 'cleanup_sub_folders')
    def test_backup(self, mock_cleanup, mock_archive, mock_dump):
        folder = Folder(config)
        folder.backup()
        self.assertTrue(mock_cleanup.called)
        self.assertTrue(mock_archive.called)
        self.assertTrue(mock_dump.called)
