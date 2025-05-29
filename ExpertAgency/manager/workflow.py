from envs.cinde.Lib.msilib.schema import tables

from ExpertAgency.experts.table_selection import TableSelectionExpert
from MataDataServices.manager import MetaDataManger
from ExpertAgency.experts.entity_extraction import EntityExtractionAgent
from ExpertAgency.experts.entity_match import EntityMatchExpert

class QNAWorkFlow:
    def __init__(self, request):
        self.request = request
        self.metadata_manager = MetaDataManger()


    def run(self):
        """
        Run the workflow for a given question.
        1. table setection
        """
        user_prompt = self.request.get("user_prompt", "")
        table_metadata = self.metadata_manager.get_metadata_table()
        if not table_metadata:
            return {"error": "No table metadata available."}

        # Initialize the table selection expert
        table_selection_expert = TableSelectionExpert(self.request)
        tables = table_selection_expert.run(table_metadata)
        print(f'total number of tables found : {len(tables)} \n tables : {tables}')
        # Return the result from the table selection expert
        # Get the entity extraction agent
        entity_extraction_agent = EntityExtractionAgent()
        entity = entity_extraction_agent.extract(user_query=user_prompt)
        print(f'Entity extraction result: {entity}')
        params = []
        for item in tables:
            params.append({
                "name": item.get("name"),
                "question_part": item.get("question_part"),
                "entity": entity
            })
        entity_matches_obj = EntityMatchExpert(params=params)
        entity_matches = entity_matches_obj.match_entities()
        return entity_matches
