from MataDataServices.metadata.factroy import MetaDataSchemaFactory
from MataDataServices.metadata.TableMeta import TABLE_METADATA

class MetaDataManger:
    def __init__(self):
        """
        Initialize the MetaDataManager.
        """
        pass

    def get_metadata_schema(self,source):
        """
        Fetch metadata for a given key from the source.
        """
        meta_data = MetaDataSchemaFactory.get(source)
        return meta_data or []

    def get_metadata_table(self):
        """
        Fetch metadata table for a given key from the source.
        """
        return TABLE_METADATA or []
