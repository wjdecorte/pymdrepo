"""
repository.operators.workflow_operators - Database operations for workflow related tables

@author - jwd3

@copyright:  2017 Equifax. All rights reserved.

@license:    Apache License 2.0

@contact:    jason.decorte@equifax.com

Version History:
0.1.1 jwd3 02/06/2017
    Updated get_parameter_value to use _select so connections are closed
"""
import os
import sys

from repository.operators.base_operator import BaseOperator
from repository.metadata.models import WorkflowConfig
from sqlalchemy import and_

__version__ = "0.1.1"
__date__ = '1/24/2017'
__updated__ = '02/06/2017'
__all__ = []


class WorkflowConfigOperator(BaseOperator):
    """ Operations on the Workflow Config table"""
    db_table_class = WorkflowConfig
    
    def get_parameter_value(self,workflow_name,parameter_name):
        result = self.select_one(workflow_name=workflow_name,parameter_name=parameter_name)
        return result.get('parameter_value')
