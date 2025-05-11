class AnswerGenerator:
    def __init__(self, client):
        self.client = client

    def generate_answer(self, query, relevant_documents):
        prompt = f"Question: {query}\n\nRelevant Documents:\n"
        for doc in relevant_documents:
            prompt += f"- {doc}\n"
        prompt += "\nProvide a detailed and helpful response."

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text.strip()