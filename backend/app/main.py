"""SĀRTHI — Sanskrit AI Research & Teaching Helper Interface (Backend)."""

import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.act.router import process as act_process
from app.models.chat import ChatRequest
from app.services import (
    dictionary_service,
    translation_service,
    grammar_service,
    sentence_service,
    sandhi_service,
    shloka_service,
    quiz_service,
    lesson_service,
)

app = FastAPI(title="SĀRTHI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- models ----------
class TranslateRequest(BaseModel):
    text: str
    direction: str = "auto"  # auto | san2en | en2san

class MeaningRequest(BaseModel):
    word: str

class AnalyzeRequest(BaseModel):
    sentence: str

class SandhiRequest(BaseModel):
    text: str


# ---------- health ----------
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "Sarthi Sanskrit Bot",
        "version": "1.0.0",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "message": "Sarthi is running and ready to help you learn Sanskrit"
    }


# ---------- chat (ACT pipeline) ----------
@app.post("/api/chat")
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(400, "Message cannot be empty.")
    return act_process(
        req.message,
        conversation_history=[message.model_dump() for message in req.conversation_history],
        learner_context=req.learner_context,
    )


# ---------- translate ----------
@app.post("/api/translate")
def translate(req: TranslateRequest):
    if not req.text.strip():
        raise HTTPException(400, "Text cannot be empty.")
    result = translation_service.handle(req.text)
    return result


# ---------- word meaning ----------
@app.post("/api/meaning")
def meaning(req: MeaningRequest):
    if not req.word.strip():
        raise HTTPException(400, "Word cannot be empty.")
    return dictionary_service.handle(req.word)


# ---------- grammar ----------
@app.post("/api/grammar")
def grammar(req: ChatRequest):
    return grammar_service.handle(req.message)

@app.get("/api/grammar/topics")
def grammar_topics():
    return grammar_service.get_all_topics()

@app.get("/api/grammar/topics/{topic_id}")
def grammar_topic(topic_id: str):
    t = grammar_service.get_topic(topic_id)
    if not t:
        raise HTTPException(404, "Topic not found.")
    return t


# ---------- sentence analysis ----------
@app.post("/api/analyze-sentence")
def analyze_sentence(req: AnalyzeRequest):
    if not req.sentence.strip():
        raise HTTPException(400, "Sentence cannot be empty.")
    return sentence_service.handle(req.sentence)


# ---------- sandhi ----------
@app.post("/api/sandhi")
def sandhi(req: SandhiRequest):
    return sandhi_service.handle(req.text)

@app.get("/api/sandhi")
def sandhi_all():
    return sandhi_service.get_all()


# ---------- shlokas ----------
@app.get("/api/shlokas")
def shlokas():
    return shloka_service.get_all()

@app.get("/api/shlokas/{shloka_id}")
def shloka(shloka_id: int):
    s = shloka_service.get_by_id(shloka_id)
    if not s:
        raise HTTPException(404, "Shloka not found.")
    return s


# ---------- lessons ----------
@app.get("/api/lessons")
def lessons():
    return lesson_service.get_all()

@app.get("/api/lessons/{lesson_id}")
def lesson(lesson_id: int):
    l = lesson_service.get_by_id(lesson_id)
    if not l:
        raise HTTPException(404, "Lesson not found.")
    return l


# ---------- quiz ----------
@app.get("/api/quiz")
def quiz(count: int = 10, category: str | None = None):
    return quiz_service.get_questions(count, category)


# ---------- dictionary ----------
@app.get("/api/dictionary")
def dictionary():
    return dictionary_service.get_all()
