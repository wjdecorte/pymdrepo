"""
<PATH> file_cleanup_operator - <DESCRIPTION>

Version History:

"""
from repository.operators.base_operator import BaseOperator
from repository.metadata.models import FileCleanup

__version__ = "0.1"
__date__ = '2/24/2017'
__updated__ = '2/24/2017'
__all__ = []


class FileCleanupOperator(BaseOperator):
    """
    Defines methods and attributes for database operations on the File Cleanup table
    """
    db_table_class = FileCleanup
