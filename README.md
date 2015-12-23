# pidropi

Simple backup library which I made for my Raspberry Pi

This library is able to backup data from file system / mysql.
You can specify databases and folders you'd like to backup in the config file.
Actually it is possible to use a dictionary as a config.
As an example you can check `pidropy.py` script in the root derectory of the project.
This script backup in temporary folder up to N times (outdated backups will be removed) 
then it will archive it and sync with your dropbox. 
Backup uses mysqldump and rsync for backups creation.
Library will create separate folder in the temporary folder for each backup type: `sql` for the mysql dumps and `fodlers` for the folders
It needs dropbox application to be ready. In order to create application visit `developers` section on dropbox whebsite:
https://www.dropbox.com/developers
Then go to `My Apps` and create the new `Dropbox API` app. It is recommended to choose `App folder` so application will have stricted access only to his folder
After you will finish with making, you wil be able to `Generated access token`, you will need this token to configure the project

This library was tested with python 2.7 which is default for the Pi.

### Configure ###

Check confing.ini file.

Required for the mysql backups
- **databases**
 - **mysql** comma separated list of databases to backup
- **mysql** Credentials for mysql
 - **login**  
 - **passwd**
 - **host**

Required for the dirs backups
- **folders**
 - **folders** comma separated list of the directories to backup

Required for all setups
- **tmp**
 - **tmpFolder** absolute path to the temporary folder. In this folder lib store backups
 - **subFolder** files limit for the temporary folder. Library will cleanup outdated files
- **dropbox**
 - **token** token from the dropbox applications

### Install ###

You might need to install the following libraries on you Pi in order to fulfill lib requirements.
This particular packages are required for the cffi, which is a part of requests[security]
```bash
$ sudo apt-get install libffi-dev
$ sudo apt-get install python-dev
```

This will require a sudo, it won't work with --user parameter
```bash
sudo pip install -r requirements.txt
```
It took ages for me (about 7 minutes)

### Test ###

Install the following packages
```bash
$ pip install mock
$ pip install nose && nosetests
```
And then just run 
```bash
$ nosetests
```
in the project root