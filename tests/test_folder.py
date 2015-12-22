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

    def test_init_single_folder(self):
        folder = Folder(config)
        self.assertEqual(folder.folders, config['folders']['folders'].split(','))

    def test_set_folders_multiple_folders(self):
        config_changed = copy.deepcopy(config)
        config_changed['folders']['folders'] = '/tmp/1,/tmp/2'
        folder = Folder(config_changed)
        self.assertEqual(folder.folders,
                         [x.strip() for x in config_changed['folders']['folders'].split(',')])

        config_changed['folders']['folders'] = '/tmp/1, /tmp/2,/tmp/3,    /tmp/4'
        folder = Folder(config_changed)
        self.assertEqual(folder.folders,
                         [x.strip() for x in config_changed['folders']['folders'].split(',')])

    @mock.patch('backup.folder.call')
    @mock.patch('backup.backup.os')
    def test_dump_folders(self, mock_os, mock_call):
        folder = Folder(config)
        folder.dump_folders()
        self.assertTrue(mock_os.mkdir.called)
        self.assertTrue(mock_call.called)
