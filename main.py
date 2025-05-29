from ExpertAgency.manager.workflow import QNAWorkFlow


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    request = {
        "user_id": "123",
        "user_prompt": "Show me companies with high opportunity scores that we should prioritize for outreach",
        "scope": "...",
        "context": {}
    }
    workflow = QNAWorkFlow(request)
    result = workflow.run()
