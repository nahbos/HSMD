import faiss
import numpy as np

class SemanticCache:
    def __init__(self, dimension=3072, threshold=0.9):
        self.index = faiss.IndexFlatIP(dimension)
        self.responses = []
        self.queries = []
        self.embeddings = []
        self.threshold = threshold

    def get_embeddings(self, texts):
        embeddings = []
        for text in texts:
            # Check if the embedding is already cached
            if text in self.embedding_cache:
                embeddings.append(self.embedding_cache[text])  # Use cached embedding
            else:
                # If not cached, make the API call to get the embedding
                response = self.client.models.embed_content(
                    model="gemini-embedding-exp-03-07",
                    contents=[text]
                )
                embedding = response.embeddings[0].values
                embeddings.append(embedding)
                # Store the embedding in cache
                self.embedding_cache[text] = embedding
        return embeddings

    def query(self, document_handler, query):
        if query in self.queries:
            embedding = self.embeddings[self.queries.index(query)]
        else: 
            embedding = np.array([document_handler.get_embeddings([query])[0]]).astype('float32')

        scores, indices = self.index.search(embedding, 1)
        if scores[0][0] >= self.threshold:
            return self.responses[indices[0][0]], embedding
        
        if not self.responses:
            return None, embedding
        
        return None, embedding

    def store(self, query, embedding, response):
        self.index.add(np.array([embedding]).astype('float32'))
        self.responses.append(response)
        self.queries.append(query)
        self.embeddings.append(embedding)