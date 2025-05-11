def should_query_llm(similarity_scores, threshold=0.85):
    return max(similarity_scores) < threshold