import os
import numpy as np
import faiss
import asyncio

class DocumentHandler:
    def __init__(self, client, data_folder="./data/"):
        self.client = client
        self.data_folder = data_folder
        self.documents = []
        self.embeddings = []
        self.index = None

    async def load_documents(self):
        txt_files = [f for f in os.listdir(self.data_folder) if f.endswith('.txt')]
        self.documents = []
        for file in txt_files:
            with open(os.path.join(self.data_folder, file), 'r') as f:
                self.documents.append(f.read())

    async def get_embeddings(self, texts):
        response = await asyncio.to_thread(self.client.models.embed_content, 
                                            model="gemini-embedding-exp-03-07", 
                                            contents=texts)
        return [embedding.values for embedding in response.embeddings]
    
    async def index_documents(self):
        self.embeddings = await self.get_embeddings(self.documents)
        embeddings_array = np.array(self.embeddings).astype('float32')
        
        # self.index = faiss.IndexFlatL2(embeddings_array.shape[1])
        self.index = self.create_hnsw_index(dimension=embeddings_array.shape[1])        
        self.index.add(embeddings_array)

    def create_hnsw_index(self, dimension=768, ef_construction=40, M=32):
        index = faiss.IndexHNSWFlat(dimension, M)
        index.hnsw.efConstruction = ef_construction
        return index
    
    def get_document_embeddings(self):
        return self.embeddings

    def get_faiss_index(self):
        return self.index