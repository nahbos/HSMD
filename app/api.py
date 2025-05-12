import nest_asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
import threading

from app.retrieval import RetrievalSystem
from app.answer_generator import AnswerGenerator
from optimizations.semantic_cache import SemanticCache

nest_asyncio.apply()
app = FastAPI()

retrieval_system = None
answer_generator = None

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(req: QuestionRequest):
    query = req.question
    query_embedding = document_handler.get_embeddings([query])[0]
    cached_answer = semantic_cache.query(query_embedding)

    if cached_answer:
        answer = cached_answer
        print('Answered by semantic cache.')
    else:
        relevant_docs = retrieval_system.search(query, top_k=3)
        answer = answer_generator.generate_answer(query, relevant_docs)
        semantic_cache.store(query_embedding, answer)
        print('Answered by Gemini.')

    return JSONResponse(content={"answer": answer})

def run_app():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def start_api(doc_handler, client):
    global retrieval_system, answer_generator, document_handler, semantic_cache
    semantic_cache = SemanticCache(dimension=3072)
    document_handler = doc_handler
    retrieval_system = RetrievalSystem(doc_handler)
    answer_generator = AnswerGenerator(client)
    thread = threading.Thread(target=run_app, daemon=True)
    thread.start()