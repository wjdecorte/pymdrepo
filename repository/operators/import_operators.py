"""
repository.operators.import_operators.py - Operators used for import tables in metadata repository

Version History:
0.2 jxv71 1/25/2017
    Updated ImportFileDownloadLogOperator.get_new_file_downloads
0.3 jwd3 1/26/2017
    Added ImportODSLogOperator
    Added ImportStageLogOperator.get_new_stage_loads
0.3.1 jwd3 1/30/2017
    Removed ImportStageLogOperator.get_new_stage_loads - no longer needed
0.3.2 jwd3 02/06/2017
    Changed StatusTableOperator to LogTableOperator
"""
from repository.metadata.models import ImportDefinition, ImportFileDownloadLog, ImportStageLog, ImportODSLog
from repository.operators.base_operator import BaseOperator, LogTableOperator

__version__ = "0.3.2"
__date__ = '01/24/2017'
__updated__ = '02/06/2017'
__all__ = []


class ImportDefinitionOperator(BaseOperator):
    """
    Defines methods and attributes for database operations on the ImportDefinition table
    """
    db_table_class = ImportDefinition

    # def get_source_by_name(self, source_name):
    #     """
    #     Get a source ingestion record by source name
    #     :param source_name: Name of source
    #     :return: Instance of the Table class representing one record
    #     """
    #     return self.session.query(self.db_table_class).filter_by(source_name=source_name).one()
    #

    def get_source_record_list(self,source_group_name):
        return self.select(source_group_name=source_group_name)


class ImportFileDownloadLogOperator(LogTableOperator):
    """
    Defines methods and attributes for database operations on the ImportFileDownloadLog table
    """
    db_table_class = ImportFileDownloadLog

    def get_new_file_downloads(self,**kwargs):
        if not self.session:
            self.get_session()

        stage_ids = (self.session.query(ImportStageLog.id).join(ImportDefinition)
                      .filter(ImportStageLog.status == 'complete',
                              ImportDefinition.source_group_name == 'doubleclick'))
        new_file_download_ids = (self.session.query(ImportFileDownloadLog.id).join(ImportDefinition)
                                  .filter(ImportFileDownloadLog.status == 'complete',
                                          ImportDefinition.source_group_name == 'doubleclick')
                                  .except_(stage_ids))
        new_file_download_id_records = new_file_download_ids.all()
        new_file_download_records = (self.session.query(ImportFileDownloadLog)
              .filter(ImportFileDownloadLog.id.in_([x[0] for x in new_file_download_id_records])))
        return new_file_download_records.all()


class ImportStageLogOperator(LogTableOperator):
    """
    Defines methods and attributes for database operations on the ImportStageLog table
    """
    db_table_class = ImportStageLog


class ImportODSLogOperator(LogTableOperator):
    """
    Defines methods and attributes for database operations on the ImportODSLog table
    """
    db_table_class = ImportODSLog
