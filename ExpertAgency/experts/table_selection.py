from ExpertAgency.resource.llm_tools import LLMTools

class TableSelectionExpert:
    def __init__(self,request):
        """
        Initialize the TableSelectionExpert.
        """
        self.request = request
        self.llm = LLMTools()

    def generate_table_selection_prompts(self,user_prompt,table_metadata):
        # Format the table descriptions for prompt inclusion
        table_descriptions = "\n".join([
            f"- **{table['name']}**: {table['description']}"
            for table in table_metadata
        ])

        system_prompt = f"""You are an expert database assistant that helps in identifying which tables are needed to answer a user’s natural language question.

        You are provided with:
        1. A list of tables, each with a `name` and `description`.
        2. A user question.
    
        Your task is to:
        - Understand the user’s question by splitting it into one or more **semantic parts** (question_parts).
        - For each question_part, determine which table(s) are required based on their descriptions.
        - Return a list of dictionaries, where each dictionary includes:
          - `name`: the relevant table name.
          - `question_part`: the exact portion of the user's question that maps to this table.
    
        Rules:
        - Make sure to select the 'organization' table if the question involves companies or organizations.
        - Only select tables that are **necessary** to answer the question.
        - If multiple tables are needed, list each separately with the corresponding question part.
        - Do not assume relationships between tables unless clearly implied in the question.
    
        Here are the available tables:
        {table_descriptions}
        """

        user_prompt_template = f"User prompt: \"{user_prompt}\""

        return system_prompt, user_prompt_template

    def run(self,table_metadata):
        """
        Run the table selection expert with the provided metadata.
        """
        user_prompt = self.request.get("user_prompt", "")
        system_prompt, user_prompt_template = self.generate_table_selection_prompts(user_prompt, table_metadata)
        result = self.llm.chat_completion(
            [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            structured_output=True,
        )
        # Here you would typically call an LLM or another service to process the prompts
        # For demonstration, we will return the prompts directly
        return result.get('response', [])

