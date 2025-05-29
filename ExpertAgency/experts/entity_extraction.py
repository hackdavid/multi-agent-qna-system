import json
import logging
from typing import List, Dict, Optional
from ExpertAgency.resource.llm_tools import LLMTools

class EntityExtractionAgent:
    def __init__(self):
        """
        :param llm: An LLM object with a `chat_completion()` method that supports `structured_output=True`
        """
        self.llm = LLMTools()
        self.system_prompt = self._build_system_prompt()
        self.few_shot_examples = self._build_few_shots()

    def _build_system_prompt(self) -> str:
        return (
            "You are an intelligent entity extraction agent. Your job is to analyze natural language queries "
            "and convert them into a structured output for data processing.\n\n"
            "Output must strictly follow this JSON format:\n"
            "{\n"
            '  "filters": [],\n'
            '  "groupby": [],\n'
            '  "orderby": {metrics :"asc" | "desc"},\n'
            '  "focused_metrics": [],\n'
            '  "date_range": "",\n'
            '  "limit": "<int>"\n'
            "}\n\n"
            "Definitions:\n"
            "- filters: entities like company names, regions, or any specific context\n"
            "- groupby: grouping fields like region, company, category, etc.\n"
            "- orderby: focus metrics and sorting direction if the prompt suggests rank or order\n"
            "- focused_metrics: metrics of interest (e.g., revenue, sales)\n"
            "- date_range: temporal range mentioned in the prompt\n"
            "- limit: explicit number if mentioned (e.g., top 5, 10 records)\n\n"
            "Always return valid JSON. Use [] or \"\" for empty values.\n"
        )

    def _build_few_shots(self) -> List[Dict[str, str]]:
        examples = [
            {
                "user_query": "Show me top 3 companies by profit in 2023",
                "structured_output": {
                    "filters": [],
                    "groupby": ["company"],
                    "orderby": {"profit": "desc"},
                    "focused_metrics": ["profit"],
                    "date_range": "2023",
                    "limit": "3"
                }
            },
            {
                "user_query": "Show me companies with high opportunity scores that we should prioritize for outreach",
                "structured_output": {
                    "filters": [""],
                    "groupby": ["companies"],
                    "orderby": {"opportunity scores": "desc"},
                    "focused_metrics": ["opportunity scores","outreach"],
                    "date_range": "",
                    "limit": ""
                }
            },
        ]
        messages = []
        for ex in examples:
            messages.append(
                {"role": "user", "content": f'Extract structured fields from this user query:\n"{ex["user_query"]}"'})
            messages.append({"role": "assistant", "content": json.dumps(ex["structured_output"], indent=2)})
        return messages

    def extract(self, user_query: str) -> Optional[Dict]:
        """
        Extract structured fields from the user query.
        """
        try:
            messages = [{"role": "system", "content": self.system_prompt}] + self.few_shot_examples
            messages.append(
                {"role": "user", "content": f'Extract structured fields from this user query:\n"{user_query}"'})

            result = self.llm.chat_completion(messages=messages, structured_output=True)

            return result.get("response") if isinstance(result, dict) else None
        except Exception as e:
            logging.exception("Entity extraction failed.")
            return None
