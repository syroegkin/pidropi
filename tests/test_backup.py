import mock
import unittest
import copy

from backup.backup import Backup
from fixtures import config


class TestBackup(unittest.TestCase):

    def setUp(self):
        """Initializer, unittest-style"""
        super(TestBackup, self).setUp()

    def tearDown(self):
        """Destructor, unittest-style"""
        super(TestBackup, self).tearDown()

    @mock.patch.object(Backup, 'set_tmp_folder')
    def test_init_backup_defaults(self, mock_set_folder):
        config_changed = copy.deepcopy(config)
        del config_changed['tmp']
        backup = Backup(config_changed)
        # Just check we got defaults
        self.assertEqual(backup.subFoldersNum, backup.subFoldersNumDefault)
        self.assertTrue(mock_set_folder.called)

    @mock.patch.object(Backup, 'set_tmp_folder')
    def test_init_backup_with_config(self, mock_set_folder):
        backup = Backup(config)
        self.assertEqual(backup.subFoldersNum, config['tmp']['subFolders'])
        self.assertTrue(mock_set_folder.called)

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
        current_time = (2015, 12, 20, 23, 26, 30, 6, 354, 0)
        folder_name = backup.create_current_folder_by_time(current_time)
        self.assertTrue(mock_os.mkdir.called)
        self.assertEqual(folder_name, ''.join(str(x) for x in current_time[:6]))

    @mock.patch('backup.backup.call')
    @mock.patch('backup.backup.os')
    @mock.patch('backup.backup.rmtree')
    @mock.patch('backup.backup.os.path')
    def test_archive_with_directories(self, mock_path, mock_rmtree, mock_os, mock_call):
        mock_os.listdir.return_value = ['123123123', '234234234']
        mock_path.isdir.return_value = True
        backup = Backup(config)
        backup.archive()
        self.assertTrue(mock_os.listdir.called)
        self.assertTrue(mock_call.called)
        self.assertTrue(mock_rmtree.called)

    @mock.patch('backup.backup.call')
    @mock.patch('backup.backup.os')
    @mock.patch('backup.backup.rmtree')
    @mock.patch('backup.backup.os.path')
    def test_archive_without_directories(self, mock_path, mock_rmtree, mock_os, mock_call):
        backup = Backup(config)
        backup.archive()
        self.assertTrue(mock_os.listdir.called)
        self.assertFalse(mock_call.called)
        self.assertFalse(mock_rmtree.called)

    @mock.patch('backup.backup.os')
    @mock.patch('backup.backup.os.path')
    def test_cleanup_sub_folders_with_directories_less_than_required(self, mock_path, mock_os):
        mock_os.listdir.return_value = ['123123123', '234234234']
        mock_path.isfile.return_value = True
        backup = Backup(config)
        backup.cleanup_sub_folders()
        self.assertTrue(mock_os.listdir.called)
        self.assertFalse(mock_os.remove.called)

    @mock.patch('backup.backup.os')
    @mock.patch('backup.backup.os.path')
    def test_cleanup_sub_folders_with_directories(self, mock_path, mock_os):
        mock_os.listdir.return_value = ['1', '2', '3', '4', '5', '6', '7', '8']
        mock_path.isfile.return_value = True
        backup = Backup(config)
        backup.cleanup_sub_folders()
        self.assertTrue(mock_os.listdir.called)
        self.assertTrue(mock_os.remove.called)
