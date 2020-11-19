"""
repository/__init__.py - Repository package initialization

Version History:
0.2 jwd3 1/11/2017
    Added check for environment variable for password file location
0.2.1 jwd3 02/27/2017
    Updated path to password module
    Removed defaults for base_dir and mdrepo_db_host
"""
import os

from .utils.password import Password

__version__ = "0.2.1"
__date__ = '2016-12-14'
__updated__ = '02/27/2017'


base_dir = os.environ.get('MDREPO_DB_PFILE')
if not base_dir:
    raise EnvironmentError("Missing environment variable MDREPO_DB_PFILE")
mdrepo_db_host = os.environ.get('MDREPO_DB_HOST')
if not mdrepo_db_host:
    raise EnvironmentError("Missing environment variable MDREPO_DB_HOST")
mdrepo_db_user = os.environ.get('MDREPO_DB_USER') or 'mdrepo'
password = Password(host=mdrepo_db_host,username=mdrepo_db_user,data_file_name='.repo',data_file_dir=base_dir)

db_url = 'postgresql+psycopg2://{user}:{pswd}@{host}:5432/loadmgrdb'
METADATA_DATABASE_URL = db_url.format(user=mdrepo_db_user,
                                      pswd=password.decrypt(),
                                      host=mdrepo_db_host)
