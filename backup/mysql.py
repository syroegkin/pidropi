from subprocess import call
from backup.backup import Backup
import time
import os


class Mysql(Backup):
    """
    Mysql dump and backup
    """

    databases = []

    mysqlLogin = None
    mysqlPasswd = None
    mysqlHost = None

    tmpPostfix = 'sql'

    def __init__(self, config):
        """Constructor
        :param config:
        """

        super().__init__(config)

        # Checking first is everything is ok with config
        if 'databases' not in config or 'mysql' not in config['databases']:
            raise ValueError('No mysql, nothing to work with')
        if 'mysql' not in config:
            raise ValueError('Mysql connect details are necessary')

        if 'tmp' not in config or 'tmpFolder' not in config['tmp']:
            raise ValueError('Tmp folder is required for this job')

        # Getting databases list information
        self.set_databases(config['databases']['mysql'])

        # Getting mysql connection information
        self.set_mysql_credentials(config['mysql'])

        # Setting tmp folder
        self.set_tmp_folder(config['tmp']['tmpFolder'])

        # Clean up old folders
        self.cleanup_sub_folders()

    def backup(self):
        """
        Make backup
        """
        self.dump_databases()

    def set_databases(self, databases):
        """Set up databases list to backup
        :param databases: string, list of databases divided by comma
        """
        if len(databases) == 0:
            raise ValueError('databases might be a string')
        self.databases = map(str.strip, databases.split(','))

    def set_mysql_credentials(self, cred):
        """Set up mysql login/pass for connection
        :param cred: dictionary with mysql connection info
        """
        if 'passwd' not in cred or 'login' not in cred or 'host' not in cred:
            raise ValueError('Not enough data for mysql')
        self.mysqlLogin = cred['login']
        self.mysqlHost = cred['host']
        self.mysqlPasswd = cred['passwd']

    def set_tmp_folder(self, folder):
        """
        Set up tmp folder, plus assigning sql postfix
        :param folder: Tmp folder
        """
        self.tmpFolder = folder + '/' + self.tmpPostfix
        super(Mysql, self).set_tmp_folder(self.tmpFolder)

    def dump_databases(self):
        """Backup with mysqldump"""
        folder_name = time.strftime("%Y%M%d%H%M%S")
        os.mkdir(self.tmpFolder + '/' + folder_name)
        for database in self.databases:
            call(['mysqldump',
                  '-u' + self.mysqlLogin,
                  '-p' + self.mysqlPasswd,
                  '-h' + self.mysqlHost,
                  '-r' + self.tmpFolder + '/' + folder_name + '/' + database + '.sql',
                  "%s" % database
                  ])
