import faiss
import numpy as np
import pickle
import threading
import time

class SemanticCache:
    def __init__(self, dimension=3072, threshold=0.9, cache_file='caches.pkl'):
        self.index = faiss.IndexFlatIP(dimension)
        self.threshold = threshold
        self.cache_file = cache_file
        self.queries, self.embeddings, self.responses = self.load_cache()
        self.flag = 0
        self.save_thread = threading.Thread(target=self.periodically_save_cache, daemon=True)
        self.save_thread.start()

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
        self.index.add(embedding)
        self.responses.append(response)
        self.queries.append(query)
        self.embeddings.append(embedding)
        self.flag = 1

    def load_cache(self):
        try:
            with open(self.cache_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return [], [] ,[]

    def save_cache(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump((self.queries, self.embeddings, self.responses), f)

    def periodically_save_cache(self):
        while True:
            if self.flag == 1:
                time.sleep(2 * 60)  # Wait for 5 minutes (300 seconds)
                self.save_cache()  # Save the cache every 5 minutes
                self.flag = 0
                print("Cache saved to disk.")