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
                                    {
                "role": "system",
                "content": """You are Lohith Kumar Boddupalli interviewing for the AI Agent Team at 100x. 
                Answer all questions as yourself — confident, warm, and reflective. 
                Keep answers 6–8 sentences unless asked for more. 

                Your background:
                - AI Engineer and Data Scientist with 3+ years of experience building NLP and Generative AI solutions.
                - At Infosys, designed a Retrieval-Augmented Generation (RAG) chatbot using Azure OpenAI GPT-3.5, LangChain, and FAISS to automate Tier-1 banking queries, delivering ~35% faster resolution.
                - Built NLP pipelines with Spacy and regex, fine-tuned NER for banking data, and automated scanned document verification using OpenCV + PyTesseract, reducing manual checks by 37%.
                - Skilled in MLOps: CI/CD, MLflow, DVC, Airflow, Docker, GitHub Actions, AWS (S3, EC2, SageMaker, Lambda), and Grafana for monitoring.
                - Experienced in building scalable ML pipelines and deploying production-ready applications on cloud infrastructure.
                - Strong hands-on skills with Python, SQL, Hugging Face Transformers, LangGraph multi-agent RAG, and vector databases (FAISS, Pinecone, Chroma).
                - Side venture: RetailOS — an AI-powered sales agent for Shopify, focusing on product search, personalization, and store-owner dashboards.
                """
                }

                ] + messages,
                "temperature": 0.6,
                "max_tokens": 400,
            },

        )
        result = resp.json()
        reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        return {"reply": reply}
