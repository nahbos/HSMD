import faiss
import numpy as np

class SemanticCache:
    def __init__(self, dimension=3072, threshold=0.9):
        self.index = faiss.IndexFlatIP(dimension)
        self.responses = []
        self.threshold = threshold

    def query(self, embedding):
        if not self.responses:
            return None
        embedding = np.array([embedding]).astype('float32')
        scores, indices = self.index.search(embedding, 1)
        if scores[0][0] >= self.threshold:
            return self.responses[indices[0][0]]
        return None

    def store(self, embedding, response):
        self.index.add(np.array([embedding]).astype('float32'))
        self.responses.append(response)