from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from app.stocks import answer_stock_question 
from flask_cors import CORS
app = FastAPI()

origins = [
    "http://localhost:5000",
    "localhost:5000",
    "127.0.0.1:5000",
    "http://127.0.0.1:5000",
    "http://localhost:3000",
    "localhost:3000",
    "127.0.0.1:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
CORS(app)
@app.post("/ask")
async def ask(request: Request) -> dict:
    data = await request.json()
    question = data['question']
    print(question)
    generated_text = "answer"
    generated_text = answer_stocks_question(question)
    return {
        "data": { generated_text }
    }
