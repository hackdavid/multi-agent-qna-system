from MataDataServices.metadata.schemas.organization import OrganizationSchema
from MataDataServices.metadata.schemas.opportunity_assements import OPPORTUNITY_ASSEMENT


class MetaDataSchemaFactory:
    _schemas = {
        'organization': OrganizationSchema,
        'opportunity_assessments': OPPORTUNITY_ASSEMENT
    }

    @classmethod
    def get(cls,source):
        """
        Fetch metadata schema for a given source.
        """
        if source in cls._schemas:
            return cls._schemas[source]
        else:
            return []
