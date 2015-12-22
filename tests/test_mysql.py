import mock
import copy
import unittest

from backup.mysql import Mysql
from fixtures import config


class TestMysql(unittest.TestCase):

    def test_init_with_wrong_config(self):
        config_changed = copy.deepcopy(config)
        del config_changed['databases']
        with self.assertRaises(ValueError):
            Mysql(config_changed)

        config_changed = copy.deepcopy(config)
        del config_changed['mysql']
        with self.assertRaises(ValueError):
            Mysql(config_changed)

    @mock.patch.object(Mysql, 'set_databases')
    @mock.patch.object(Mysql, 'set_mysql_credentials')
    def test_init_correct_config(self, mock_creds, mock_databases):
        Mysql(config)
        self.assertTrue(mock_creds.called)
        self.assertTrue(mock_databases.called)

    def test_set_databases_error(self):
        mysql = Mysql(config)
        with self.assertRaises(ValueError):
            mysql.set_databases('')

    def test_set_databases_correct(self):
        mysql = Mysql(config)
        mysql.set_databases(config['databases']['mysql'])
        self.assertEqual(mysql.databases, config['databases']['mysql'].split(','))

        databases = 'db1,    db2, db3,db4'
        mysql.set_databases(databases)
        self.assertEqual(mysql.databases, [x.strip() for x in databases.split(',')])

    def test_my_credentials_error(self):
        mysql = Mysql(config)
        with self.assertRaises(ValueError):
            mysql.set_mysql_credentials([])

    def test_my_credentials(self):
        mysql = Mysql(config)
        self.assertEqual(mysql.mysqlLogin, config['mysql']['login'])
        self.assertEqual(mysql.mysqlHost, config['mysql']['host'])
        self.assertEqual(mysql.mysqlPasswd, config['mysql']['passwd'])

    @mock.patch.object(Mysql, 'dump_databases')
    @mock.patch.object(Mysql, 'archive')
    @mock.patch.object(Mysql, 'cleanup_sub_folders')
    def test_backup(self, mock_cleanup, mock_archive, mock_dump):
        mysql = Mysql(config)
        mysql.backup()
        self.assertTrue(mock_cleanup.called)
        self.assertTrue(mock_archive.called)
        self.assertTrue(mock_dump.called)

    @mock.patch.object(Mysql, 'create_current_folder_by_time')
    @mock.patch('backup.mysql.call')
    def test_dump_databases(self, mock_call, mock_create):
        mysql = Mysql(config)
        mysql.dump_databases()
        self.assertTrue(mock_create.called)
        self.assertTrue(mock_call.called)
