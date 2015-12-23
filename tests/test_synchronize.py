import mock
import copy
import unittest

from dropbox.exceptions import ApiError
from backup.synchronize import Synchronize
from fixtures import config


class TestMysql(unittest.TestCase):

    def test_init_wrong_data(self):
        config_changed = copy.deepcopy(config)
        del config_changed['dropbox']
        with self.assertRaises(ValueError):
            Synchronize(config_changed)

    @mock.patch('backup.synchronize.dropbox')
    def test_init(self, mock_dropbox):
        sync = Synchronize(config)
        self.assertTrue(mock_dropbox.Dropbox.called)
        self.assertEqual(sync.tmpFolder, config['tmp']['tmpFolder'])

    @mock.patch('__builtin__.open')
    @mock.patch('backup.synchronize.os')
    @mock.patch('backup.synchronize.os.path')
    @mock.patch('backup.synchronize.dropbox')
    def test_sync(self, mock_dropbox, mock_path, mock_os, mock_open):
        mock_dropbox.Dropbox.return_value = mock_dropbox
        mock_dropbox.users_get_current_account.return_value = True
        mock_dropbox.files.WriteMode.overwrite = 2
        e = ApiError('abc', 'cdf', 'efg')
        mock_dropbox.files_get_metadata.side_effect = e
        mock_os.walk.return_value = [
            ('./file1.txt', [], ['43a9100fbc512ef82e5f96c8c88447cd546c34f'])
        ]
        mock_path.return_value = True

        sync = Synchronize(config)
        sync.sync()

        self.assertTrue(mock_dropbox.files_upload.called)

