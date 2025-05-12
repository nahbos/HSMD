# **RAG-Powered Question-Answering system via Telegram Bot**

This project implements a **Retrieval-Augmented Generation (RAG)**-based question-answering system accessible via a **Telegram bot**. The system ingests documents, retrieves relevant context based on user input, and generates responses using an LLM (Gemini).

## **Architecture Overview**

The architecture of the system consists of the following main components:
1. **Backend**: A REST API built with **FastAPI** that exposes an `/ask` endpoint.
2. **Document Handling**: Loads `.txt` documents from the `./data/` folder, performs vector search using **FAISS** indexing (with **HNSW**).
3. **LLM Integration**: Uses **Gemini API** to generate answers based on the relevant context retrieved from documents.
4. **Telegram Bot**: A **Telegram bot** that allows users to interact with the question-answering system.
5. **Containerization**: The entire application is containerized using **Docker** for easy deployment.
6. **Optimization**: Implemented strategies to reduce API calls, caching of answers, and response latency.

## **Project Structure**

RAG-Telegram-Bot/
│
├── app/ # Main application folder
│ ├── api.py # FastAPI backend with /ask endpoint
│ ├── answer_generator.py # Logic for generating answers using LLM
│ ├── document_handler.py # Handles document loading and indexing
│ ├── retrieval.py
│ ├── semantic_cache.py # Caching logic for pre-computed answers
│ └── telegram_bot.py # Telegram bot integration
│
├── data/ # Folder where the .txt documents are stored
│ └── commons.txt
│ └── literature.txt
│
├── requirements.txt # List of Python dependencies
└── README.md # Project documentation
