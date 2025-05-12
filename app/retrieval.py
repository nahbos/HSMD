import numpy as np

class RetrievalSystem:
    def __init__(self, document_handler):
        self.document_handler = document_handler
        self.index = document_handler.get_faiss_index()
        self.documents = document_handler.documents

    def search(self, embedding, top_k=3):
        query_embedding = np.array(embedding).astype('float32').reshape(1, -1)
        distances, indices = self.index.search(query_embedding, top_k)
        result_documents = [self.documents[i] for i in indices[0]]
        return result_documents