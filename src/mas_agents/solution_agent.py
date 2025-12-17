class SolutionAgent(BaseAgent):
    def __init__(self, client):
        super().__init__(client, name="SolutionAgent")

    def process(self, fetched_data, diagnosis):
        self.log_action("Generating solution")

        system_prompt = """
You are a Solution Agent for IT support. Based on the diagnosis and fetched data, provide a comprehensive solution.
Return this exact JSON structure:
{
    solution: "detailed solution steps",
    tools_needed: ["list", "of", "tools", "or", "resources"],
    estimated_time: "time to resolve the issue"
}
"""
    messages = [
        {"role": "user", "content": f"Fetched Data: {json.dumps(fetched_data)}\nDiagnosis: {json.dumps(diagnosis)}"}
    ]
    resposne = self.call_claude(messages, system_prompt)
    if not response:
        self.log_action("Failed to get response from Claude")
        return None
    try:
        solution = json.loads(response)
        self.log_action("Successfully generated solution")
        return solution
    except json.JSONDecodeError as e:
        self.log_action(f"Failed to parse JSON: {e}")
        self.log_action(f"Raw response: {response}")
        return None
