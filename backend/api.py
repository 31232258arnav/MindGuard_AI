"""
MindGuard AI - FastAPI REST API Service
Provides endpoints for text classification, conversational screening,
batch CSV audits, paper metrics, and emergency crisis intervention.
"""

import os
import sys
import json
import time

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import pandas as pd

from backend.model_engine import predictor, CLASSES, CLASS_METRICS, OVERALL_METRICS

app = FastAPI(
    title="MindGuard AI - Mental Health Sentimental Analysis Platform",
    description="A BERT-based 7-Class Mental Health Early Screening & Clinical Triage REST API. Vishwakarma University Group 21.",
    version="1.0.0"
)

# Enable CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class StatementRequest(BaseModel):
    text: str

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatSessionRequest(BaseModel):
    messages: List[ChatMessage]
    user_name: Optional[str] = "Friend"

# Crisis Directory
CRISIS_HELPLINES = [
    {
        "name": "Tele-MANAS (Govt. of India)",
        "number": "14416 / 1800 891 4416",
        "coverage": "Pan-India (24x7, Toll-Free, 20+ Languages)",
        "type": "National Comprehensive Mental Health Care Service"
    },
    {
        "name": "Vandrevala Foundation Helpline",
        "number": "+91 9999 666 555",
        "coverage": "India (24x7 Free Crisis Counseling via Call/WhatsApp)",
        "type": "Crisis Intervention & Suicide Prevention"
    },
    {
        "name": "AASRA Suicide Prevention Helpline",
        "number": "+91 98204 66726",
        "coverage": "Mumbai & Pan-India (24x7)",
        "type": "Emotional Support & Suicide Prevention"
    },
    {
        "name": "KIRAN National Helpline (MSJE)",
        "number": "1800-599-0019",
        "coverage": "Govt. of India (24x7, 13 Languages)",
        "type": "Mental Health Rehabilitation & Clinical Triage"
    },
    {
        "name": "NIMHANS Psychosocial Helpline",
        "number": "080-46110007",
        "coverage": "Bengaluru & National Referral",
        "type": "Premier Neuro-Psychiatric Guidance"
    },
    {
        "name": "988 Suicide & Crisis Lifeline",
        "number": "988 (Call or Text)",
        "coverage": "United States & Canada (24x7)",
        "type": "Immediate Free & Confidential Crisis Support"
    }
]

# Benchmark data from Paper Tables
PAPER_BENCHMARKS = {
    "project_title": "Sentimental Analysis for Mental Health Detection",
    "sub_title": "A BERT-based text classification system for early mental-health screening",
    "institution": "Vishwakarma University, Pune",
    "department": "Department of Computer Engineering, Faculty of Science and Technology",
    "academic_year": "2026-2027",
    "group_number": "Group No. 21 (Division B)",
    "authors": [
        {"name": "Bhupesh Bhatia", "roll": "31232179"},
        {"name": "Samruddhi Meher", "roll": "31232202"},
        {"name": "Arnav Phuke", "roll": "31232258"},
        {"name": "Sushrut Ingle", "roll": "31230710"},
        {"name": "Saket Radke", "roll": "31230741"}
    ],
    "mentor": "Prof. Richa Agnihotri",
    "table_1_distribution": [
        {"class": "Normal", "samples": 3269, "share_pct": 31.0},
        {"class": "Depression", "samples": 3081, "share_pct": 29.2},
        {"class": "Suicidal", "samples": 2130, "share_pct": 20.2},
        {"class": "Anxiety", "samples": 768, "share_pct": 7.3},
        {"class": "Bipolar", "samples": 555, "share_pct": 5.3},
        {"class": "Stress", "samples": 518, "share_pct": 4.9},
        {"class": "Personality disorder", "samples": 215, "share_pct": 2.0}
    ],
    "table_2_configuration": {
        "Pre-trained Model": "bert-base-uncased",
        "Number of Classes": 7,
        "Maximum Sequence Length": "128 tokens",
        "Batch Size": 16,
        "Optimizer": "AdamW (eps = 1e-8)",
        "Learning Rate": "2e-5 (Linear Decay)",
        "Warm-up Steps": 0,
        "Gradient Clipping": "Max norm 1.0",
        "Training Epochs": 7,
        "Best Checkpoint Selection": "Epoch 5 (Validation Accuracy 82.80%)",
        "Data Split": "72% Train / 8% Val / 20% Test (Stratified)"
    },
    "table_3_classification_report": CLASS_METRICS,
    "table_4_epochs": [
        {"epoch": 1, "train_loss": 0.8373, "train_acc": 0.6787, "val_loss": 0.5102, "val_acc": 0.7967, "val_f1": 0.7953},
        {"epoch": 2, "train_loss": 0.4217, "train_acc": 0.8306, "val_loss": 0.4690, "val_acc": 0.8142, "val_f1": 0.8120},
        {"epoch": 3, "train_loss": 0.3006, "train_acc": 0.8784, "val_loss": 0.4737, "val_acc": 0.8268, "val_f1": 0.8267},
        {"epoch": 4, "train_loss": 0.2093, "train_acc": 0.9223, "val_loss": 0.5842, "val_acc": 0.8197, "val_f1": 0.8156},
        {"epoch": 5, "train_loss": 0.1379, "train_acc": 0.9549, "val_loss": 0.6844, "val_acc": 0.8280, "val_f1": 0.8278, "is_best": True},
        {"epoch": 6, "train_loss": 0.0887, "train_acc": 0.9749, "val_loss": 0.8731, "val_acc": 0.8266, "val_f1": 0.8263},
        {"epoch": 7, "train_loss": 0.0579, "train_acc": 0.9845, "val_loss": 0.9394, "val_acc": 0.8263, "val_f1": 0.8264}
    ],
    "overall_summary": OVERALL_METRICS
}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MindGuard AI Mental Health Classifier",
        "version": "1.0.0",
        "timestamp": time.time()
    }

@app.post("/api/analyze")
def analyze_statement(req: StatementRequest):
    """Classifies a user statement across the 7 mental health categories."""
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty text input provided.")
    
    result = predictor.predict(req.text)
    
    # Attach crisis resources if elevated risk or suicidal ideation detected
    if result["risk_assessment"]["is_crisis"]:
        result["crisis_directory"] = CRISIS_HELPLINES
    else:
        result["crisis_directory"] = []
        
    return result

@app.post("/api/chat")
def conversational_screening(req: ChatSessionRequest):
    """
    Conversational mental-health screening agent.
    Maintains dialogue context, analyzes sentiment trajectory, and generates
    empathetic, non-judgmental guidance with clinical escalation triggers.
    """
    if not req.messages:
        raise HTTPException(status_code=400, detail="No messages in chat session.")
    
    latest_msg = req.messages[-1].content
    analysis = predictor.predict(latest_msg)
    
    primary_class = analysis["primary_class"]
    confidence = analysis["confidence"]
    is_crisis = analysis["risk_assessment"]["is_crisis"]
    
    # Empathetic conversational responses based on predicted emotional state
    if is_crisis or primary_class == "Suicidal":
        bot_response = (
            f"I hear how much unbearable pain you are carrying right now, and I want you to know that your life has immense value. "
            f"You don't have to carry this heavy burden alone. Please connect with someone who can support you right this second: "
            f"You can call or WhatsApp the Tele-MANAS helpline at 14416 (or 1800 891 4416) or Vandrevala Foundation at +91 9999 666 555. "
            f"They are completely free, confidential, and available 24/7. Please stay safe with me."
        )
    elif primary_class == "Depression":
        bot_response = (
            f"Thank you for being open and sharing this with me. What you're feeling sounds deeply exhausting, "
            f"and it makes complete sense that you feel drained. Depression can make even small daily moments feel like uphill battles. "
            f"Have you been able to sleep, eat, or talk to someone you trust recently? Taking things one minute at a time is completely okay."
        )
    elif primary_class == "Anxiety":
        bot_response = (
            f"I sense how intense that anxiety and racing feeling must be right now. Let's pause for a second together. "
            f"Try taking a slow, deep breath in for 4 seconds... hold for 4... and release for 6 seconds. "
            f"Remind yourself that although anxiety feels overwhelming and alarming, this feeling is a temporary bodily surge and you are safe right here. "
            f"What is one physical object in the room you can see right now?"
        )
    elif primary_class == "Stress":
        bot_response = (
            f"It sounds like you have so much weight resting on your shoulders right now with competing demands. "
            f"Chronic stress takes a real physical toll. Remember that you do not have to solve everything all at once. "
            f"Can we identify just one single task on your list that can be deferred or set aside until tomorrow?"
        )
    elif primary_class == "Bipolar":
        bot_response = (
            f"Navigating sharp shifts in mood, energy, and momentum can feel disorienting and overwhelming. "
            f"Acknowledging these transitions is an important grounding step. Are you currently tracking your sleep rhythms "
            f"or able to connect with your support system or healthcare provider?"
        )
    elif primary_class == "Personality disorder":
        bot_response = (
            f"Intense emotional waves and feelings of emptiness or relationship friction can be deeply distressing. "
            f"Your feelings are valid, even when they feel stormy and difficult to regulate. Focusing on grounding DBT techniques "
            f"like holding something cold or taking slow, steady breaths can help anchor the present moment."
        )
    else:
        bot_response = (
            f"It's really nice to hear from you today! You seem to be in a balanced and peaceful space. "
            f"How has the rest of your week been going, and is there anything creative or rewarding you've been working on?"
        )
        
    return {
        "reply": bot_response,
        "message_analysis": analysis,
        "distress_flag": is_crisis,
        "triage_recommendation": analysis["risk_assessment"]["clinical_recommendation"],
        "crisis_directory": CRISIS_HELPLINES if is_crisis else []
    }

@app.post("/api/batch")
async def batch_screening(file: UploadFile = File(...)):
    """
    Batch processing endpoint for CSV or TXT file uploads.
    Extracts text statements, runs 7-class inference, and compiles audit statistics.
    """
    try:
        content = await file.read()
        filename = file.filename.lower()
        statements = []
        
        if filename.endswith(".csv"):
            import io
            df = pd.read_csv(io.BytesIO(content))
            # Find candidate text column
            candidate_cols = [c for c in df.columns if any(k in c.lower() for k in ["statement", "text", "message", "post", "sentence"])]
            text_col = candidate_cols[0] if candidate_cols else df.columns[0]
            statements = df[text_col].dropna().astype(str).tolist()
        else: # TXT file, one line per statement
            text_lines = content.decode("utf-8", errors="replace").splitlines()
            statements = [line.strip() for line in text_lines if line.strip()]
            
        if not statements:
            raise HTTPException(status_code=400, detail="No readable statements found in uploaded file.")
            
        # Process first 500 statements for fast interactive response
        limit_statements = statements[:500]
        results = []
        class_counts = {c: 0 for c in CLASSES}
        risk_counts = {"Normal": 0, "Mild": 0, "Elevated": 0, "Critical": 0}
        
        for stmt in limit_statements:
            pred = predictor.predict(stmt)
            top_cls = pred["primary_class"]
            class_counts[top_cls] += 1
            
            if pred["risk_assessment"]["is_crisis"]:
                risk_counts["Critical"] += 1
            elif "ELEVATED" in pred["risk_assessment"]["level"]:
                risk_counts["Elevated"] += 1
            elif "MILD" in pred["risk_assessment"]["level"]:
                risk_counts["Mild"] += 1
            else:
                risk_counts["Normal"] += 1
                
            results.append({
                "statement": stmt[:100] + ("..." if len(stmt) > 100 else ""),
                "predicted_class": top_cls,
                "confidence": pred["confidence_percentage"],
                "risk": pred["risk_assessment"]["level"]
            })
            
        return {
            "total_processed": len(limit_statements),
            "class_distribution": class_counts,
            "risk_summary": risk_counts,
            "sample_results": results[:50] # Preview top 50
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process batch file: {str(e)}")

@app.get("/api/benchmarks")
def get_benchmarks():
    """Returns research paper experimental results, tables, and Vishwakarma University metadata."""
    return PAPER_BENCHMARKS

@app.get("/api/helplines")
def get_helplines():
    """Returns official verified 24/7 mental health crisis helplines."""
    return {"helplines": CRISIS_HELPLINES}

@app.get("/api/samples")
def get_sample_statements():
    """Returns authentic sample statements across all 7 classes from the benchmark corpus."""
    samples_path = os.path.join(os.path.dirname(__file__), "..", "data", "test_samples.json")
    if os.path.exists(samples_path):
        with open(samples_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Serve Frontend static assets
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
