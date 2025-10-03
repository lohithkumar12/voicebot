from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os, httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    messages = data.get("messages", [])
    if not messages:
        return {"reply": "No input received."}

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}",
                     "Content-Type": "application/json"},
                        json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": """You are Lohith Kumar Boddupalli interviewing for the AI Agent Team at 100x. 
            Answer all questions as yourself — confident, warm, and reflective. 
            Keep answers 6–8 sentences unless asked for more. 
            Your background: 
            - Senior System Engineer / Data Scientist at Infosys (BFSI, 3+ years). 
            - Built NLP pipelines (Spacy NER, regex, OCR) with PostgreSQL. 
            - Built RAG & Agentic prototypes (LangGraph/LangChain), FAISS/Pinecone. 
            - MLOps experience (DVC, MLflow, Docker, GitHub Actions, AWS/GCP). 
            - Side venture: RetailOS, AI sales agent for Shopify. 
            """}
                ] + messages,
                "temperature": 0.6,
                "max_tokens": 400,
            },

        )
        result = resp.json()
        reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        return {"reply": reply}
