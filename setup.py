from distutils.core import setup

setup(
        name='pidropi',
        version='1.0.0',
        packages=['backup'],
        url='',
        license='',
        author='syroegkin',
        author_email='',
        description='Dropbox backup tool for Pi',
        install_requires=[
            'configparser2==4.0',
            'dropbox==4.0',
            'requests==2.8.1',
            'urllib3==1.12',
            'path.py==8.1.2'
        ]
)
