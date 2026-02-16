import time
from fastapi import FastAPI
from search import search_similar
from llm import generate
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()

@app.get("/ask")
def ask(question: str):
    start = time.time()
    context = search_similar(question)
    logging.info(f"Tempo do search: {time.time() - start:.2f}s")

    start2 = time.time()
    answer = generate(context, question)
    logging.info(f"Tempo do generate: {time.time() - start2:.2f}s")

    return {"answer": answer}


