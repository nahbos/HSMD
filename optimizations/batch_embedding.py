import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def embed_texts(texts, batch_size=16):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        encoded = tokenizer(batch, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            output = model(**encoded)
        batch_embeddings = output.last_hidden_state.mean(dim=1)
        embeddings.extend(batch_embeddings.cpu().numpy())
    return np.array(embeddings)