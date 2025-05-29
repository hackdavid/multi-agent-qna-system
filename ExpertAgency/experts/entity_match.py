from MataDataServices.manager import MetaDataManger
from ExpertAgency.resource.llm_tools import LLMTools
from typing import List, Dict
import json

class EntityMatchExpert:
    '''
    This class will get the entity from params and match the entities
    1. focus metrics with the table metadata
    2. order by metrics with the table metadata
    3. groupby metrics with the table metadata
    4. filters with the table metadata

    '''
    def __init__(self, params):
        self.params = params
        self.metadata_manager = MetaDataManger()
        self.llm = LLMTools()

    def validate_groupby(self, groupby_fields: List[str], source_meta_data: List[Dict[str, str]]) -> List[str]:
        """
        Validate and match group-by fields using metadata and LLM.

        :param groupby_fields: List of group-by fields from user prompt (e.g., ["region", "category"])
        :param source_meta_data: List of metadata dicts with keys: key, label, description
        :return: List of valid `key`s to group by
        """
        try:
            system_prompt = (
                "You are a helpful assistant for data transformation. Your task is to match user-requested 'group by' fields "
                "to metadata columns.\n\n"
                "Each column in metadata has:\n"
                "- key: technical column name\n"
                "- label: human-friendly column name\n"
                "- description: explanation of the field\n\n"
                "Given a list of user group-by fields, match them to the best metadata entries based on label or description. "
                "Return a Python list of only the `key`s that match.\n"
                "Ignore fields that don't match.\n"
            )

            meta_str = "\n".join(
                f"- key: {m['key']}, label: {m['label']}, description: {m['description']}"
                for m in source_meta_data
            )

            user_prompt = (
                f"User group-by fields: {', '.join(groupby_fields)}\n\n"
                f"Available metadata:\n{meta_str}\n\n"
                "Return a list of matching metadata `key`s:"
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            result = self.llm.chat_completion(messages=messages, structured_output=True)

            return result.get("response") if isinstance(result.get("response"), list) else []

        except Exception as e:
            return []

    def get_validated_metrics(self, metrics: List[str], source_meta_data: List[Dict[str, str]]) -> List[str]:
        """
        Given a list of extracted metrics and metadata for columns, use the LLM to validate and return
        the list of valid metric keys from the metadata.

        :param metrics: List of extracted metric names (e.g., ["profit", "sales"])
        :param source_meta_data: List of dicts with keys: 'key', 'label', 'description'
        :return: List of valid 'key's from the metadata matching the metrics
        """
        try:
            system_prompt = (
                "You are a data reasoning assistant. Your job is to match user-provided metrics with a metadata table.\n\n"
                "Each metadata entry has:\n"
                "- name: actual column name used in the database\n"
                "- label: human-readable name\n"
                "- description: explanation of what the column represents\n\n"
                "Match each user metric to the most relevant column(s) using label and description. "
                "Return only a list of matching `name`s. If nothing matches, return an empty list.\n\n"
                "Always return a Python list of strings.\n"
            )

            meta_str = "\n".join(
                f"- key: {m['name']}, label: {m['label']}, description: {m['description']}"
                for m in source_meta_data
            )

            user_prompt = (
                f"User metrics: {', '.join(metrics)}\n\n"
                f"Available metadata:\n{meta_str}\n\n"
                "Return the list of matching column keys:"
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            result = self.llm.chat_completion(messages=messages, structured_output=True)

            return result.get("response") if isinstance(result.get("response"), list) else []

        except Exception as e:
            return []

    def validate_orderby(self, orderby_data: Dict[str, str], source_meta_data: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Validate the orderby metrics using LLM based on metadata.

        :param orderby_data: Dict like {"sales": "desc"} from user input
        :param source_meta_data: List of column metadata with keys: key, label, description
        :return: Dict with matched metric keys and directions, e.g., {"total_sales": "desc"}
        """
        try:
            system_prompt = (
                "You are a data column reasoning assistant. Your job is to match ordering metrics from user input "
                "to actual database column keys using the provided metadata.\n\n"
                "Each metadata entry has:\n"
                "- key: the column name in the database\n"
                "- label: user-friendly column name\n"
                "- description: details about the column\n\n"
                "You will be given a dictionary of metrics and sort direction (asc/desc) from the user. "
                "Return a dictionary where keys are the matching column `key`s from the metadata, and values are the directions.\n\n"
                "Only include keys from metadata. Do not include unmatched fields.\n"
            )

            meta_str = "\n".join(
                f"- key: {m['key']}, label: {m['label']}, description: {m['description']}"
                for m in source_meta_data
            )

            user_prompt = (
                f"User orderby request: {json.dumps(orderby_data)}\n\n"
                f"Available metadata:\n{meta_str}\n\n"
                "Return a dictionary with matching column keys and their respective order directions."
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            result = self.llm.chat_completion(messages=messages, structured_output=True)

            return result.get("response") if isinstance(result.get("response"), dict) else {}

        except Exception as e:
            return {}

    def match_entities(self):
        """
        Match the entities in params with the table metadata.
        """
        final_params = []
        for param in self.params:
            entity = param.get('entity',{})
            temp_params = {}
            source = param.get('name', None)
            source_meta_data = self.metadata_manager.get_metadata_schema(source)
            # validate focus_metrics
            focus_metrics = entity.get('focused_metrics', [])
            if focus_metrics:
                valid_focus_metrics = self.get_validated_metrics(focus_metrics, source_meta_data)
                temp_params['focused_metrics'] = valid_focus_metrics

            # lets validate the groupby metrics
            orderby = entity.get('orderby', {})
            if orderby:
                valid_orderby = self.validate_orderby(orderby, source_meta_data)
                temp_params['orderby'] = valid_orderby
            # lets match and validate the groupby
            groupby = entity.get('groupby', [])
            if groupby:
                valid_groupby = self.validate_groupby(groupby, source_meta_data)
                temp_params['groupby'] = valid_groupby

            final_params.append(temp_params)
        return final_params


