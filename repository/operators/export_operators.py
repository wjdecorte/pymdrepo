"""
repository.operators.export_operators.py - Operators used for export tables in metadata repository

@author - joji varughese

@copyright:  2017 Equifax. All rights reserved.

@license:    Apache License 2.0

@contact:    joji.varughese@equifax.com

Version History:
0.1 jxv71 2/6/2017
    Initial Version
0.1.1 jwd3 2/7/2017
    Changed StatusTableOperator to LogTableOperator
"""
from repository.metadata.models import ExportDefinition, ExportLog
from repository.operators.base_operator import BaseOperator, LogTableOperator

__version__ = "0.1.1"
__date__ = '02/06/2017'
__updated__ = '02/07/2017'
__all__ = []


class ExportDefinitionOperator(BaseOperator):
    """
    Defines methods and attributes for database operations on the ExportDefinition table
    """
    db_table_class = ExportDefinition


class ExportLogOperator(LogTableOperator):
    """
    Defines methods and attributes for database operations on the ExportLog table
    """
    db_table_class = ExportLog
