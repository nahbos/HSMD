import faiss
import numpy as np

def create_hnsw_index(dimension=768, ef_construction=40, M=32):
    index = faiss.IndexHNSWFlat(dimension, M)
    index.hnsw.efConstruction = ef_construction
    return index

def add_to_index(index, vectors):
    index.add(np.array(vectors).astype('float32'))

def search_index(index, query_vector, top_k=5):
    query_vector = np.array([query_vector]).astype('float32')
    D, I = index.search(query_vector, top_k)
    return D, I