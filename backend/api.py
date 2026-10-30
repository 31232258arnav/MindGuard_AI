"""
MindGuard AI - FastAPI REST API Service & Clinical Intelligence Backend
MindGuard AI Research Initiative.

Features:
- Fast 7-class BERT-based mental health classification
- LangChain Structured Clinical MindBot Brain with boundaries and real-life soothing
- Multi-format file analysis (PDF, DOCX, CSV, TXT)
- Crisis helplines directory and emergency triage guardrails
- Full academic benchmarks and validation metrics
"""

import os
import sys
import json
import time
import asyncio
import io
import re
from typing import List, Optional, Dict, Any

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd

from backend.model_engine import predictor, CLASSES, CLASS_METRICS, OVERALL_METRICS
from backend.langchain_brain import (
    generate_langchain_clinical_response,
    generate_intelligent_clinical_fallback,
    CRISIS_HELPLINES
)
from backend.file_analyzer import analyze_document_mental_health, sanitize_pii, generate_soap_note

app = FastAPI(
    title="MindGuard AI - Mental Health Sentimental Analysis Platform",
    description="A BERT-based 7-Class Mental Health Early Screening & Clinical Triage REST API. MindGuard AI Research Initiative.",
    version="2.0.0"
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
    api_key: Optional[str] = None
    custom_model: Optional[str] = None

# Benchmark data from Paper Tables
PAPER_BENCHMARKS = {
    "project_title": "Sentimental Analysis for Mental Health Detection",
    "sub_title": "A BERT-based text classification system for early mental-health screening",
    "institution": "Vishwakarma University, Pune",
    "department": "Department of Computer Engineering, Faculty of Science and Technology",
    "academic_year": "2026-2027",
    "group_number": "Clinical AI Research Consortium",
    "authors": [
        {"name": "Lead ML Engineer", "roll": "RES-2026-02"},
        {"name": "Psychometric Research Specialist", "roll": "RES-2026-03"},
        {"name": "Core System Architect", "roll": "RES-2026-01"},
        {"name": "Backend Systems Engineer", "roll": "RES-2026-04"},
        {"name": "Clinical UI Specialist", "roll": "RES-2026-05"}
    ],
    "mentor": "Clinical NLP & Cognitive Systems Advisory Board",
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
        "version": "2.0.0",
        "features": [
            "BERT 7-Class Prediction",
            "LangChain Structured Clinical Brain",
            "Multi-Format Document File Analyzer (PDF/DOCX/CSV/TXT)",
            "Dynamic Real-Life Soothing & Curative Protocols"
        ],
        "timestamp": time.time()
    }

@app.post("/api/analyze")
def analyze_statement(req: StatementRequest):
    """Classifies a user statement across the 7 mental health categories."""
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Empty text input provided.")
    
    clean_text = sanitize_pii(req.text)
    result = predictor.predict(clean_text)
    
    # Attach crisis resources if elevated risk or suicidal ideation detected
    if result["risk_assessment"]["is_crisis"]:
        result["crisis_directory"] = CRISIS_HELPLINES
    else:
        result["crisis_directory"] = []
        
    return result

def calculate_psychometrics(text: str, history: List[ChatMessage] = None) -> Dict[str, Any]:
    """Computes cognitive distortions, emotional valence, and somatic arousal."""
    text_lower = text.lower()
    
    # 1. Distortions
    distortions = []
    if any(k in text_lower for k in ["ruined", "disaster", "catastrophe", "worst", "end of my life", "hopeless"]):
        distortions.append("Catastrophizing")
    if any(k in text_lower for k in ["always", "never", "everyone", "nobody", "completely", "total failure"]):
        distortions.append("All-or-Nothing Thinking")
    if any(k in text_lower for k in ["they think", "they hate me", "everyone is judging", "they must believe"]):
        distortions.append("Mind Reading")
    if any(k in text_lower for k in ["my fault", "i caused this", "i ruined it", "because of me", "blame myself"]):
        distortions.append("Personalization")
    if any(k in text_lower for k in ["nothing ever", "every single time", "always like this", "never works"]):
        distortions.append("Overgeneralization")
    if not distortions:
        distortions.append("Contextual Distress (No Distortions)")

    # 2. Emotional Valence (-1.0 to +1.0)
    neg_words = ["hate", "terrible", "sad", "pain", "hurts", "crying", "hopeless", "anxious", "scared", "panic", "fail", "dying", "tired", "empty", "alone", "worthless"]
    pos_words = ["happy", "good", "great", "better", "peace", "calm", "hope", "proud", "love", "relieved", "grateful", "fine", "okay", "excited"]
    neg_count = sum(1 for w in neg_words if w in text_lower)
    pos_count = sum(1 for w in pos_words if w in text_lower)
    valence = round(max(-1.0, min(1.0, (pos_count - neg_count) * 0.25 - 0.2 if neg_count > 0 else (pos_count * 0.3))), 2)

    # 3. Somatic Arousal / Agitation (0% to 100%)
    arousal = 35
    if any(k in text_lower for k in ["panic", "racing", "heart", "shaking", "sweat", "cannot breathe", "hyperventilate", "chest", "terror"]):
        arousal += 40
    if "!" in text or "?" in text:
        arousal += min(20, text.count("!") * 5 + text.count("?") * 3)
    if any(k in text_lower for k in ["urgent", "right now", "immediately", "screaming", "collapsing", "dying"]):
        arousal += 20
    arousal = min(100, arousal)

    # 4. Emotional Trajectory
    trajectory = "Baseline Initialized"
    if history and len(history) > 1:
        user_msgs = [m.content for m in history if m.role == "user"]
        if len(user_msgs) > 1:
            prev_v = calculate_psychometrics(user_msgs[-2])["valence_score"]
            delta = round(valence - prev_v, 2)
            if delta > 0.15:
                trajectory = f"Improving (+{delta})"
            elif delta < -0.15:
                trajectory = f"Escalating Distress ({delta})"
            else:
                trajectory = "Stable Emotional Cadence"

    # 5. Tailored Soothing Prescription
    if arousal > 65:
        prescription = "4-7-8 Vagal Nerve Paced Breathing & Cold Water Facial Reset (Diver's Reflex)"
    elif "Catastrophizing" in distortions or "Mind Reading" in distortions:
        prescription = "CBT Evidence-Testing Reframe (Objective Fact vs Emotion Log)"
    elif valence < -0.4:
        prescription = "Behavioral Micro-Step & Non-Judgmental Self-Compassion Anchor"
    else:
        prescription = "5-4-3-2-1 Sensory Grounding & Mindful Reflection"

    return {
        "distortions_detected": distortions,
        "valence_score": valence,
        "arousal_index": f"{arousal}%",
        "trajectory": trajectory,
        "prescribed_soothing": prescription
    }

@app.post("/api/chat")
async def conversational_screening(req: ChatSessionRequest):
    """
    Conversational mental-health screening agent with live LangChain AI Brain & calculating power.
    Maintains dialogue context, computes cognitive distortions, and delivers structured clinical output.
    """
    if not req.messages:
        raise HTTPException(status_code=400, detail="No messages in chat session.")
    
    for m in req.messages:
        m.content = sanitize_pii(m.content)
    latest_msg = req.messages[-1].content
    analysis = predictor.predict(latest_msg)
    
    # Run Calculating Power Module
    psychometrics = calculate_psychometrics(latest_msg, req.messages)
    
    # Generate structured AI Brain response via LangChain
    structured_ai = await generate_langchain_clinical_response(
        messages=req.messages,
        analysis=analysis,
        custom_api_key=req.api_key,
        user_name=req.user_name or "Friend"
    )
    
    # Backwards compatibility and rich structured output
    response_payload = {
        **structured_ai,
        "reply": structured_ai.get("dialogue_response", ""),
        "message_analysis": analysis,
        "psychometrics": psychometrics,
        "triage_recommendation": structured_ai.get("clinical_boundary", {}).get("mandatory_action", analysis["risk_assessment"]["clinical_recommendation"]),
        "crisis_directory": structured_ai.get("clinical_boundary", {}).get("helplines", CRISIS_HELPLINES if analysis["risk_assessment"]["is_crisis"] else [])
    }
    
    return response_payload


@app.post("/api/analyze-file")
async def analyze_file_endpoint(file: UploadFile = File(...)):
    """
    Upload and analyze PDF, DOCX, CSV, or TXT documents for clinical mental health assessment.
    Performs multi-level sentence classification, distortion extraction, and triage synthesis.
    """
    filename = file.filename or "uploaded_file.txt"
    ext = os.path.splitext(filename)[1].lower()
    
    valid_exts = [".pdf", ".docx", ".csv", ".txt"]
    if ext not in valid_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Supported formats: PDF, DOCX, CSV, TXT."
        )
        
    try:
        content_bytes = await file.read()
        if not content_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            
        result = analyze_document_mental_health(content_bytes, filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process and analyze file: {str(e)}")


@app.post("/api/batch")
async def batch_classification(file: UploadFile = File(...)):
    """Processes any CSV, TXT, PDF, or DOCX file for high-throughput batch classification."""
    filename = file.filename or "batch_dataset.csv"
    ext = os.path.splitext(filename)[1].lower()
    
    try:
        content_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read uploaded file: {str(e)}")
        
    if not content_bytes:
        raise HTTPException(status_code=400, detail="Uploaded batch file is empty.")

    statements = []

    # 1. Try CSV Parsing
    if ext == ".csv" or b"," in content_bytes[:500]:
        df = None
        for enc in ["utf-8", "latin-1", "cp1252"]:
            try:
                df = pd.read_csv(io.BytesIO(content_bytes), encoding=enc)
                break
            except Exception:
                continue
                
        if df is not None and not df.empty:
            text_column = None
            for candidate in ["text", "statement", "prompt", "message", "utterance", "content", "sentence"]:
                for col in df.columns:
                    if candidate in str(col).lower():
                        text_column = col
                        break
                if text_column:
                    break
                    
            if not text_column:
                for col in df.columns:
                    if df[col].dtype == object:
                        text_column = col
                        break
                        
            if text_column:
                for _, row in df.iterrows():
                    val = str(row[text_column]).strip() if pd.notna(row[text_column]) else ""
                    if len(val) > 3:
                        statements.append(val)

    # 2. Try Document / TXT / PDF / DOCX extraction if not populated by CSV
    if not statements:
        from backend.file_analyzer import extract_file_content
        try:
            full_text, meta = extract_file_content(content_bytes, filename)
            # Try lines first
            lines = [l.strip() for l in full_text.splitlines() if len(l.strip()) > 8]
            if len(lines) >= 2:
                statements = lines
            else:
                # Split by sentence boundaries
                sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', full_text) if len(s.strip()) > 8]
                statements = sentences if sentences else [full_text.strip()]
        except Exception as e:
            # Fallback raw line split
            try:
                raw_lines = [l.strip() for l in content_bytes.decode('utf-8', errors='ignore').splitlines() if len(l.strip()) > 8]
                statements = raw_lines
            except Exception:
                raise HTTPException(status_code=400, detail=f"Failed to extract statements: {str(e)}")

    if not statements:
        raise HTTPException(status_code=400, detail="Could not extract any valid statements from the file.")

    results = []
    class_counts = {c: 0 for c in CLASSES}
    crisis_flag_count = 0

    # Limit to first 250 statements for real-time responsiveness
    for idx, val in enumerate(statements[:250]):
        pred = predictor.predict(val)
        class_counts[pred["primary_class"]] += 1
        
        if pred["risk_assessment"]["is_crisis"]:
            crisis_flag_count += 1
            
        results.append({
            "row_index": idx,
            "text": val[:120] + ("..." if len(val) > 120 else ""),
            "primary_class": pred["primary_class"],
            "confidence_percentage": pred["confidence_percentage"],
            "is_crisis": pred["risk_assessment"]["is_crisis"]
        })
        
    total_processed = len(results)
    
    return {
        "status": "success",
        "total_records": total_processed,
        "total_processed": total_processed,
        "class_distribution": class_counts,
        "crisis_flags_detected": crisis_flag_count,
        "summary": f"Analyzed {total_processed} items from {filename}. Normal: {class_counts.get('Normal', 0)}, Depression: {class_counts.get('Depression', 0)}, Suicidal: {class_counts.get('Suicidal', 0)}, Anxiety: {class_counts.get('Anxiety', 0)}.",
        "records": results[:100]
    }


@app.post("/api/clinical-file-audit")
async def clinical_file_audit(file: UploadFile = File(...)):
    """
    Audits clinical notes/psychiatric intake documents and maps affective findings
    to PHQ-9 (0-27) and GAD-7 (0-21) severity scales.
    """
    filename = file.filename or "clinical_notes.txt"
    content_bytes = await file.read()
    if not content_bytes:
        raise HTTPException(status_code=400, detail="File is empty.")
    
    doc_res = analyze_document_mental_health(content_bytes, filename)
    shares = doc_res.get("affective_profile", {}).get("class_distribution_percent", {})
    dep_pct = shares.get("Depression", 0)
    anx_pct = shares.get("Anxiety", 0)
    sui_pct = shares.get("Suicidal", 0)
    stress_pct = shares.get("Stress", 0)
    
    # Calculate clinical PHQ-9 estimate (0-27)
    dep_score = int(min(27, round((dep_pct * 0.45) + (sui_pct * 0.9) + (stress_pct * 0.15))))
    if sui_pct > 5:
        dep_score = max(dep_score, 18)
    
    # Calculate clinical GAD-7 estimate (0-21)
    gad_score = int(min(21, round((anx_pct * 0.4) + (stress_pct * 0.25))))
    
    return {
        "status": "success",
        "filename": filename,
        "document_summary": doc_res.get("executive_summary", ""),
        "triage_level": doc_res.get("clinical_boundary", {}).get("triage_level", "Evaluated"),
        "estimated_phq9": dep_score,
        "estimated_gad7": gad_score,
        "high_risk_statements": doc_res.get("high_risk_statements", [])[:5],
        "class_distribution": shares,
        "soap_note": doc_res.get("soap_note", "")
    }

@app.get("/api/benchmarks")
def get_benchmarks():
    return PAPER_BENCHMARKS

@app.get("/api/helplines")
def get_helplines():
    return {"status": "success", "helplines": CRISIS_HELPLINES}


@app.post("/api/soap-note")
def generate_soap_endpoint(req: StatementRequest):
    """Generates a formal hospital-grade clinical SOAP Note from text."""
    clean_text = sanitize_pii(req.text)
    pred = predictor.predict(clean_text)
    p_class = pred["primary_class"]
    is_crisis = p_class == "Suicidal" or pred.get("risk_assessment", {}).get("is_crisis", False)
    
    distortions = [{"type": "Contextual Stress", "quote": clean_text[:40], "reframe": "Reframe"}]
    soap = generate_soap_note(
        filename="Clinical_Intake_Session.txt",
        total_words=len(clean_text.split()),
        dominant_class=p_class,
        triage_level="Acute Crisis Risk" if is_crisis else "Moderate Clinical Strain" if p_class in ["Depression", "Anxiety"] else "Safe / Baseline",
        class_shares={p_class: 100.0},
        high_risks=[{"quote": clean_text[:120], "class": p_class, "confidence": pred["confidence_percentage"]}] if is_crisis or p_class != "Normal" else [],
        distortions=distortions,
        is_crisis=is_crisis
    )
    return {"status": "success", "soap_note": soap}
