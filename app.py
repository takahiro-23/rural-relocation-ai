import json
import os
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


load_dotenv()

try:
  import google.generativeai as genai
except Exception:
  genai = None


class RecommendRequest(BaseModel):
  family: str
  budget: str
  work: str
  services: List[str]
  note: Optional[str] = ""


app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Serve the frontend from the same origin.
app.mount("/static", StaticFiles(directory="static", html=False), name="static")


@app.get("/")
def root():
  return FileResponse("index.html")


def build_prompt(payload: RecommendRequest) -> str:
  return (
    "You are a relocation advisor for families moving to rural Japan.\n"
    "Based on the user preferences, propose exactly 3 candidate areas.\n"
    "Return JSON only with keys: recommendations (array of 3 objects).\n"
    "Each recommendation must include: name, score (0-100), summary, tags (array).\n"
    f"Family: {payload.family}\n"
    f"Budget: {payload.budget}\n"
    f"Work: {payload.work}\n"
    f"Services: {', '.join(payload.services)}\n"
    f"Note: {payload.note}\n"
  )


def fallback_response() -> dict:
  return {
    "recommendations": [
      {
        "name": "信州あさひ市",
        "score": 92,
        "summary": "保育料補助と医療費助成が充実。家賃支援と移住支援金も手厚い。",
        "tags": ["子育て", "医療", "支援金"],
      },
      {
        "name": "みなみ高原町",
        "score": 88,
        "summary": "教育支援と学童が豊富。空き家バンクと家賃補助が利用しやすい。",
        "tags": ["教育", "家賃", "子育て"],
      },
      {
        "name": "ひだまり湖市",
        "score": 84,
        "summary": "リモート対応求人が多く、就業支援が豊富。医療アクセスも良好。",
        "tags": ["仕事", "医療", "教育"],
      },
    ]
  }


@app.post("/api/recommend")
def recommend(payload: RecommendRequest):
  api_key = os.getenv("GEMINI_API_KEY")
  model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
  if not api_key or not genai:
    return fallback_response()

  genai.configure(api_key=api_key)
  model = genai.GenerativeModel(model_name)
  prompt = build_prompt(payload)
  response = model.generate_content(
    prompt,
    generation_config={"response_mime_type": "application/json"},
  )
  text = response.text or ""
  try:
    return json.loads(text)
  except Exception:
    return fallback_response()
