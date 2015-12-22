from subprocess import call
from backup import Backup


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

        super(Mysql, self).__init__(config)

        # Check everything is ok with config
        if 'databases' not in config or 'mysql' not in config['databases']:
            raise ValueError('No mysql, nothing to work with')
        if 'mysql' not in config:
            raise ValueError('Mysql connect details are necessary')

        # Get databases list information
        self.set_databases(config['databases']['mysql'])

        # Get mysql connection information
        self.set_mysql_credentials(config['mysql'])

    def set_databases(self, databases):
        """Set up databases list to backup
        :param databases: string, list of databases divided by comma
        """
        self.databases = [x.strip() for x in databases.split(',')]
        if len(self.databases) == 0 or not any(self.databases):
            raise ValueError('databases might be a string')

    def set_mysql_credentials(self, cred):
        """Set up mysql login/pass for connection
        :param cred: dictionary with mysql connection info
        """
        if 'passwd' not in cred or 'login' not in cred or 'host' not in cred:
            raise ValueError('Not enough data for mysql')
        self.mysqlLogin = cred['login']
        self.mysqlHost = cred['host']
        self.mysqlPasswd = cred['passwd']

    def backup(self):
        """
        Make backup and clean up
        """
        self.dump_databases()
        self.archive()
        self.cleanup_sub_folders()

    def dump_databases(self):
        """Backup with mysqldump"""
        folder_name = self.create_current_folder_by_time()
        for database in self.databases:
            call(['mysqldump',
                  '-u' + self.mysqlLogin,
                  '-p' + self.mysqlPasswd,
                  '-h' + self.mysqlHost,
                  '-r' + self.tmpFolder + '/' + folder_name + '/' + database + '.sql',
                  "%s" % database
                  ])
