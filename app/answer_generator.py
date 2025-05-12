class AnswerGenerator:
    def __init__(self, client):
        self.client = client

    async def generate_answer(self, query, relevant_documents):
        prompt = f"Question: {query}\n\nRelevant Documents:\n"
        for doc in relevant_documents:
            prompt += f"- {doc}\n"
        prompt += "\n\nProvide a detailed and helpful response in Farsi/Persian language. Keep it user-friendly and brief. Its very important to keep the response in Farsi, whatever it is."

        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=prompt
        )

        return response.text.strip()