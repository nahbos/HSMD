def summarize_document(doc, llm_call):
    prompt = f"Summarize this document briefly:\n\n{doc}"
    return llm_call(prompt)

def build_summary_index(documents, llm_call):
    return {i: summarize_document(doc, llm_call) for i, doc in enumerate(documents)}