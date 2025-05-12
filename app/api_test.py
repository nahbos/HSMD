from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_ask_endpoint():
    question = "What is the capital of France?"
    response = client.post("/ask", json={"question": question})

    assert response.status_code == 200

    data = response.json()
    assert "answer" in data
    assert "Paris" in data["answer"]