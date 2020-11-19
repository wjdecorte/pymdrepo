"""
repository.operators.hdfs_usage_operator - Operators for database actions on the HDFS Usage tables

Version History:

"""
import os
import sys
from repository.metadata.models import HdfsDiskUsage
from repository.operators.base_operator import BaseOperator

__version__ = "0.1"
__date__ = '1/26/2017'
__updated__ = '1/26/2017'
__all__ = []


class HdfsDiskUsageOperator(BaseOperator):
    """ Operations on the HDFS Disk Usage table"""
    db_table_class = HdfsDiskUsage
