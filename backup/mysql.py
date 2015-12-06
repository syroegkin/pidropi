from subprocess import call

class Mysql:
    """
    Mysql dump and backup
    """

    databases = []

    mysql_login = None
    mysql_passwd = None
    mysql_host = None

    def __init__(self, config):
        """Constructor
        :param config:
        """
        # Checking first is everything is ok with config
        if 'databases' not in config or 'mysql' not in config['databases']:
            raise ValueError('No mysql, nothing to work with')
        if 'mysql' not in config:
            raise ValueError('Mysql connect details are necessary')

        # Getting databases list information
        self.set_databases(config['databases']['mysql'])

        # Getting mysql connection information
        self.set_mysql_credentials(config['mysql'])

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
            raise ValueError('Not enough creds for mysql')
        self.mysql_login = cred['login']
        self.mysql_host = cred['host']
        self.mysql_passwd = cred['passwd']

    def backup(self):
        """Backup with mysqldump"""
        call(["ls", "-l"])



