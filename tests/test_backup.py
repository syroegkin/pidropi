import mock
import unittest

from backup.backup import Backup
from fixtures import config


class TestBackup(unittest.TestCase):

    def setUp(self):
        """Initializer, unittest-style"""
        super(TestBackup, self).setUp()

    def tearDown(self):
        """Destructor, unittest-style"""
        super(TestBackup, self).tearDown()

    @mock.patch('backup.backup.os')
    def test_init_backup_defaults(self, mock_os):
        config_changed = config.copy()
        del config_changed['tmp']
        backup = Backup(config_changed)
        # Just check we got defaults
        self.assertEqual(backup.subFoldersNum, backup.subFoldersNumDefault)
        self.assertEqual(backup.tmpFolder, backup.tmpFolderDefault)

    @mock.patch('backup.backup.os')
    def test_init_backup_with_config(self, mock_os):
        backup = Backup(config)
        self.assertEqual(backup.subFoldersNum, config['tmp']['subFolders'])
        self.assertEqual(backup.tmpFolder, config['tmp']['tmpFolder'])

    @mock.patch('backup.backup.os.path')
    @mock.patch('backup.backup.os')
    def test_set_tmp_folder_absolute(self, mock_os, mock_path):
        mock_path.isdir.return_value = False
        tmp_folder = '/some/path/to/nowhere'
        backup = Backup(config)
        backup.set_tmp_folder(tmp_folder)
        self.assertEqual(backup.tmpFolder, tmp_folder)
        mock_path.isdir.assert_called_with(tmp_folder)
        # Temporary folder has been created
        mock_os.makedirs.assert_called_with(tmp_folder)

    def test_set_tmp_folder_relative(self):
        pass

    @mock.patch('backup.backup.os')
    def test_create_current_folder_by_time(self, mock_os):
        backup = Backup(config)
        backup.create_current_folder_by_time()
        self.assertTrue(mock_os.mkdir.called)
