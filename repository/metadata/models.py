"""
repository.metadata.models.py - Contains model definitions for tables in the Metadata Repository

@author - Jason DeCorte

@copyright:  2016 Equifax. All rights reserved.

@license:    Apache License 2.0

@contact:    jason.decorte@equifax.com

Version History:
0.2 jwd3 11/10/2016 ???
    Added WorkflowConfig model
    Added SourceIngestion model
    Added StageRun model
    Added Event model
    Added ValidValue model
0.3 jwd3 12/1/2016
    Added HdfsDiskUsage
    Added SourceIngestion, StageLoadStatus, OdsLoadStatus, DataWarehouseTable, DataWarehouseLoadStatus,
          DataExport, DataExportStatus
0.4 jwd3 1/11/2017
    Created filename path in doc string
    Added new table FileDownload
    Changed table name from StageLoadStatus to ImportStageLog
    Changed table name from OdsLoadStatus to ImportODSLog
    Changed table name from DataWarehouseTable to DataWarehouseDefinition
    Changed table name from DataWarehouseLoadStatus to DataWarehouseLog
    Changed table name from DataExportStatus to ExportLog
    Changed table name from DataExport to ExportDefinition
    Changed table name from SourceIngestion to
    Added batch number Sequence to import file download log and import stage log
0.4.1 jwd3 1/24/2017
    Fixed some indentations errors
    Fixed attribute name in __repr__ of ImportFileDownloadLog
    Added column ImportStageLog.table_name
    Removed unused import sqlalchemy.orm.query.Query and sqlalchemy.and_
    Added columns ImportDefinition.valid_from_dttm and .valid_to_dttm
0.4.2 jwd3 01/27/2017
    Removed autoincrement=False for ImportODSLog table so it would autoincrement
    Removed batch number sequence
    Removed batch number sequence from ImportFileDownloadLog and ImportStageLog
0.5 jwd3 02/06/2017
    Changed column name ExportDefinition.export_definition to config_definition
    Added export_frequency column to ExportDefinition
    Changed table name DataWarehouseLog to DataWarehouseDFLog
    Added new table DataWarehouseARLog
    Removed import of Sequence (no longer used)
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Table, Column, Integer, String, BigInteger, DateTime, Date, Boolean,
                        PickleType, JSON)

from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from datetime import datetime

__version__ = "0.5"
__date__ = '09-22-2016'
__updated__ = '02-06-2017'
__all__ = []


ModelBase = declarative_base()


class FileCleanup(ModelBase):
    __tablename__ = 'file_cleanup'

    rule_id = Column(Integer, primary_key=True)
    path = Column(String(500))
    hdfs_path_flg = Column(Boolean, default=False)
    filename_pattern = Column(String(250))
    cleanup_action = Column(String(1))
    archive_path = Column(String(500))
    hdfs_archive_path_flg = Column(Boolean, default=False)
    retention_period = Column(Integer)
    recursive_flg = Column(Boolean, default=False)
    date_append_flg = Column(Boolean, default=False)
    subdir_append_flg = Column(Boolean, default=False)
    active_flg = Column(Boolean, default=True)
    created_dttm = Column(DateTime,default=datetime.now)
    modified_dttm = Column(DateTime,default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return self.path


class WorkflowConfig(ModelBase):
    __tablename__ = 'workflow_config'

    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    workflow_name = Column(String(500))
    parameter_name = Column(String(500))
    parameter_value = Column(PickleType)

    def __repr__(self):
        return "{0}.{1}".format(self.workflow_name, self.parameter_name)


# Define the bridge table between import_definition and data_warehouse_table
source_to_dw_bridge = Table('source_to_dw_bridge', ModelBase.metadata,
                            Column('source_id', Integer, ForeignKey('import_definition.id')),
                            Column('dw_id', Integer, ForeignKey('data_warehouse_definition.id')))


class ImportDefinition(ModelBase):
    __tablename__ = 'import_definition'

    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    etag = Column(String(256))
    source_group_name = Column(String(50))
    source_name = Column(String(100))
    source_type = Column(String(10))      # File or Table or Stream
    ingest_frequency = Column(String(1))  # (D)aily, (H)ourly, (M)onthly, (F)ive Minute Interval, (Y)early, (O)n-demand
    source_definition = Column(JSON)  # Contains columns, preproc routines, validation routines, other attr
    last_value = Column(BigInteger)
    last_value_dttm = Column(DateTime)
    stage_retention_period = Column(Integer)
    monthly_rollup_age = Column(Integer)  # Data older than threshold is rolled into monthly partitions
    yearly_rollup_age = Column(Integer)  # Data older than threshold is rolled into yearly partitions (0 = no rollup)
    compression_age = Column(Integer)  # Data older is compressed (remove duplicates i.e. dcm match tables)
    ods_retention_period = Column(Integer)
    retry_count = Column(Integer)  # number of times to retry a task before failing
    retry_delay = Column(Integer)  # number of seconds before retrying an unsuccessful task
    start_delay = Column(Integer)  # number of seconds to delay starting a task after the end of the run period
    valid_from_dttm = Column(DateTime, default=datetime(1900,1,1))  # date the source definition is valid from
    valid_to_dttm = Column(DateTime, default=datetime(2020,12,31,23,59,59))  # date the source definition is valid to
    dw_tables = relationship("DataWarehouseDefinition", secondary=source_to_dw_bridge, back_populates="sources")

    def __repr__(self):
        return "{0}".format(self.source_group_name + '.' + self.source_name
                            if self.source_group_name else self.source_name)


class ImportODSLog(ModelBase):
    __tablename__ = 'import_ods_log'

    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    etag = Column(String(256))
    source_id = Column(Integer, ForeignKey("import_definition.id"))
    run_id = Column(String(50))
    status = Column(String(20))  # loading, operational
    table_name = Column(String(500))
    loaded_dttm = Column(DateTime)
    last_value = Column(BigInteger)
    last_value_dttm = Column(DateTime)
    record_count = Column(BigInteger)
    source = relationship("ImportDefinition", back_populates="ods_loads")

    def __repr__(self):
        return "{0}:{1}:{2} - {3}".format(self.id,self.table_name,self.run_id,self.status)

ImportDefinition.ods_loads = relationship("ImportODSLog", back_populates="source")


class ImportStageLog(ModelBase):
    __tablename__ = 'import_stage_log'

    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    etag = Column(String(256))
    source_id = Column(Integer, ForeignKey("import_definition.id"))
    run_id = Column(String(50))  # run value from Airflow
    status = Column(String(20))  # downloading, preprocessed, validated, staged, promoted, deleted
    realized_source_name = Column(String(500))  # can be full path and filename
    loaded_dttm = Column(DateTime)
    preprocessed_dttm = Column(DateTime)
    validated_dttm = Column(DateTime)
    deleted_dttm = Column(DateTime)
    operator_flag = Column(String(1), default='O')  # O=overwrite (def) A=Append
    record_count = Column(BigInteger)
    table_name = Column(String(500))
    source = relationship("ImportDefinition", back_populates="stage_loads")

    def __repr__(self):
        return "{0}:{1}:{2} - {3}".format(self.id,self.realized_source_name,self.run_id,self.status)

ImportDefinition.stage_loads = relationship("ImportStageLog", back_populates="source")


class ImportFileDownloadLog(ModelBase):
    __tablename__ = 'import_file_download_log'

    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    etag = Column(String(256))
    source_id = Column(Integer, ForeignKey("import_definition.id"))
    run_id = Column(String(50))  # run value from Airflow
    inbound_path = Column(String(500))
    filename = Column(String(500))
    status = Column(String(20))  # downloading, preprocessed, validated, staged, promoted, deleted
    record_count = Column(BigInteger)
    source = relationship("ImportDefinition", back_populates="file_downloads")

    def __repr__(self):
        return "{0}:{1}/{2} - ".format(self.id,self.inbound_path,self.filename)

ImportDefinition.file_downloads = relationship("ImportFileDownloadLog", back_populates="source")


class DataWarehouseDefinition(ModelBase):
    __tablename__ = 'data_warehouse_definition'

    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    etag = Column(String(256))
    subject_area = Column(String(50))
    table_name = Column(String(100))
    table_type = Column(String(10))  # Dim, Fact, Hybrid, aggregate, report???
    table_definition = Column(JSON)  # Contains columns, load directives, other attr
    last_value = Column(BigInteger)
    last_value_dttm = Column(DateTime)
    sources = relationship("ImportDefinition", secondary=source_to_dw_bridge, back_populates="dw_tables")

    def __repr__(self):
        return "{0}".format(self.table_name)


class DataWarehouseDFLog(ModelBase):
    __tablename__ = 'data_warehouse_df_log'

    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    etag = Column(String(256))
    dw_id = Column(Integer, ForeignKey("data_warehouse_definition.id"))
    run_id = Column(String(50))
    status = Column(String(20))  # loading, operational
    table_name = Column(String(500))
    loaded_dttm = Column(DateTime)
    last_value = Column(BigInteger)
    last_value_dttm = Column(DateTime)
    record_count = Column(BigInteger)
    dw_table = relationship("DataWarehouseDefinition", back_populates="dw_df_load")

    def __repr__(self):
        return "{0}:{1} - {2}".format(self.table_name, self.run_id,self.status)

DataWarehouseDefinition.dw_df_load = relationship("DataWarehouseDFLog", back_populates="dw_table")


class DataWarehouseARLog(ModelBase):
    __tablename__ = 'data_warehouse_ar_log'

    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    etag = Column(String(256))
    dw_id = Column(Integer, ForeignKey("data_warehouse_definition.id"))
    run_id = Column(String(50))
    status = Column(String(20))  # loading, operational
    table_name = Column(String(500))
    loaded_dttm = Column(DateTime)
    last_value = Column(BigInteger)
    last_value_dttm = Column(DateTime)
    record_count = Column(BigInteger)
    dw_table = relationship("DataWarehouseDefinition", back_populates="dw_ar_load")

    def __repr__(self):
        return "{0}:{1} - {2}".format(self.table_name, self.run_id, self.status)

DataWarehouseDefinition.dw_ar_load = relationship("DataWarehouseARLog", back_populates="dw_table")


class ExportDefinition(ModelBase):
    __tablename__ = 'export_definition'

    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    etag = Column(String(256))
    subject_area = Column(String(50))
    export_name = Column(String(100))
    export_frequency = Column(String(1))  # (D)aily, (H)ourly, (M)onthly, (Y)early, (O)n-demand
    config_definition = Column(JSON)  # Contains sources and columns, export directives, other attr
    last_value = Column(BigInteger)
    last_value_dttm = Column(DateTime)
    last_value_timezone = Column(String(20))

    def __repr__(self):
        return "{0}".format(self.export_name)


class ExportLog(ModelBase):
    __tablename__ = 'export_log'

    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    etag = Column(String(256))
    export_id = Column(Integer, ForeignKey("export_definition.id"))
    run_id = Column(String(50))
    status = Column(String(20))  # extracting, prepared
    export_target_name = Column(String(500))  # file_name, table_name, queue_name, etc.
    export_location = Column(String(500))  # file system, database, host, etc.
    export_as_of_dttm = Column(DateTime)  # date and time of the data as exported
    last_value = Column(BigInteger)
    last_value_dttm = Column(DateTime)
    record_count = Column(BigInteger)
    data_export = relationship("ExportDefinition", back_populates="export_run")

    def __repr__(self):
        return "{0}:{1} - ".format(self.source.source_name, self.run_id,self.status)

ExportDefinition.export_run = relationship("ExportLog", back_populates="data_export")


class Event(ModelBase):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    etag = Column(String(256))
    event_dttm = Column(DateTime)
    event_category = Column(String(30))
    event_group = Column(String(100))
    event_type = Column(String(100))
    event_subtype = Column(String(100))
    event_name = Column(String(500))
    event_action = Column(String(100))
    event_payload = Column(JSON)

    def __repr__(self):
        return "{0} - {1}".format(self.event_name,self.event_dttm)


class ValidValue(ModelBase):
    __tablename__ = 'valid_value'
    id = Column(Integer, primary_key=True)
    created_dttm = Column(DateTime, default=datetime.now)
    modified_dttm = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    category = Column(String(100))
    attribute_name = Column(String(100))
    valid_value = Column(String(500))

    def __repr__(self):
        return "{0}.{1}.{2}".format(self.category,self.attribute_name,self.valid_value)


class HdfsDiskUsage(ModelBase):
    __tablename__ = 'hdfs_disk_usage'

    id = Column(Integer, primary_key=True)
    create_dt = Column(Date)
    path = Column(String(300))
    directory_count = Column(Integer)
    file_count = Column(Integer)
    length = Column(BigInteger)
    quota = Column(String(10))
    space_quota = Column(String(10))
    space_consumed = Column(String(50))

    def __repr__(self):
        return self.path
