"""
repository.operators.dw_operators - Operators used for datawarehouse tables in metadata repository

@author - jwd3

@copyright:  2017 Equifax. All rights reserved.

@license:    Apache License 2.0

@contact:    jason.decorte@equifax.com

Version History:

"""
from repository.metadata.models import DataWarehouseDefinition, DataWarehouseDFLog, DataWarehouseARLog
from repository.operators.base_operator import BaseOperator, LogTableOperator

__version__ = "0.1"
__date__ = '2/4/2017'
__updated__ = '2/4/2017'
__all__ = []


class DataWarehouseDefinitionOperator(BaseOperator):
    """
    Defines methods and attributes for database operations on the DataWarehouseDefinition table
    """
    db_table_class = DataWarehouseDefinition

    def get_table_list(self,table_name_list):
        if not self.session:
            self.get_session()
        query = self.session.query(self.db_table_class)
        result_list = []
        for table_name in table_name_list:
            dw_table_record = query.filter_by(table_name=table_name).one()
            dw_table_dict = self.convert_to_dict(dw_table_record)
            if dw_table_record.sources:
                source_list = [self.convert_to_dict(source) for source in dw_table_record.sources]
            else:
                source_list = []
            dw_table_dict['sources'] = source_list
            result_list.append(dw_table_dict)
        self.close_session()
        return result_list


class DataWarehouseDFLogOperator(LogTableOperator):
    """
    Defines methods and attributes for database operations on the DataWarehouseDFLog table
    """
    db_table_class = DataWarehouseDFLog


class DataWarehouseARLogOperator(LogTableOperator):
    """
    Defines methods and attributes for database operations on the DataWarehouseARLog table
    """
    db_table_class = DataWarehouseARLog
