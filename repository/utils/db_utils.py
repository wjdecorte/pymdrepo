"""
<PATH> utils - <DESCRIPTION>

Version History:

"""
import os
from alembic.config import Config
from alembic import command

from repository.metadata.models import ModelBase
from repository.connection import repo_engine

__version__ = "0.1"
__date__ = '2/12/2017'
__updated__ = '2/12/2017'
__all__ = []


def initdb():
    """
    Build a repository from scratch
    :return:
    """
    ModelBase.metadata.create_all(bind=repo_engine)
    alembic_cfg = Config(os.path.join(os.getenv("VIRTUAL_ENV",os.getcwd()),"migrations/alembic.ini"))
    command.stamp(alembic_cfg, "head")
