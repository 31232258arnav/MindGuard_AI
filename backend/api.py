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

from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import pandas as pd
import requests

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
    api_key: Optional[str] = None
    custom_model: Optional[str] = None

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

def calculate_psychometrics(text: str, history: List[ChatMessage] = None) -> Dict[str, Any]:
    """Computes cognitive distortions, emotional valence, and somatic arousal."""
    text_lower = text.lower()
    
    # 1. Cognitive Distortions
    distortions = []
    if any(k in text_lower for k in ['fail', 'ruin', 'worst', 'never recover', 'end of world', 'disaster', 'mess up everything', 'ruined']):
        distortions.append('Catastrophizing')
    if any(k in text_lower for k in ['always', 'never', 'everyone', 'nobody', 'completely', 'total', 'all of them', 'nothing']):
        distortions.append('All-or-Nothing Thinking')
    if any(k in text_lower for k in ['they think', 'everyone thinks', 'judging me', 'they hate me', 'laughing at me', 'people think']):
        distortions.append('Mind Reading')
    if any(k in text_lower for k in ['i feel like a failure', 'feels hopeless', 'it feels impossible', 'feel worthless']):
        distortions.append('Emotional Reasoning')
    if any(k in text_lower for k in ['my fault', 'i caused this', 'i ruined it', 'because of me', 'blame myself']):
        distortions.append('Personalization')
    if any(k in text_lower for k in ['nothing ever', 'every single time', 'always like this', 'never works']):
        distortions.append('Overgeneralization')
    if not distortions:
        distortions.append('Contextual Distress (No Distortions)')

    # 2. Emotional Valence (-1.0 to +1.0)
    neg_words = ['hate', 'terrible', 'sad', 'pain', 'hurts', 'crying', 'hopeless', 'anxious', 'scared', 'panic', 'fail', 'dying', 'tired', 'empty', 'alone', 'worthless']
    pos_words = ['happy', 'good', 'great', 'better', 'peace', 'calm', 'hope', 'proud', 'love', 'relieved', 'grateful', 'fine', 'okay', 'excited']
    neg_count = sum(1 for w in neg_words if w in text_lower)
    pos_count = sum(1 for w in pos_words if w in text_lower)
    valence = round(max(-1.0, min(1.0, (pos_count - neg_count) * 0.25 - 0.2 if neg_count > 0 else (pos_count * 0.3))), 2)

    # 3. Somatic Arousal / Agitation (0% to 100%)
    arousal = 35
    if any(k in text_lower for k in ['panic', 'racing', 'heart', 'shaking', 'sweat', 'cannot breathe', 'hyperventilate', 'chest', 'terror', 'freaking out']):
        arousal += 40
    if '!' in text or '?' in text:
        arousal += min(20, text.count('!') * 5 + text.count('?') * 3)
    if any(k in text_lower for k in ['urgent', 'right now', 'immediately', 'screaming', 'collapsing', 'dying']):
        arousal += 20
    arousal = min(100, arousal)

    # 4. Emotional Trajectory
    trajectory = "Baseline Initialized"
    if history and len(history) > 1:
        user_msgs = [m.content for m in history if m.role == 'user']
        if len(user_msgs) > 1:
            prev_v = calculate_psychometrics(user_msgs[-2])['valence_score']
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
    elif 'Catastrophizing' in distortions or 'Mind Reading' in distortions:
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


def generate_dynamic_cbt_fallback(user_msg: str, analysis: dict, psychometrics: dict, user_name: str = "Friend") -> str:
    """Intelligent situation-aware clinical response synthesizer when offline or LLM fails."""
    t_lower = user_msg.lower()
    p_class = analysis.get("primary_class", "Normal")
    
    if any(k in t_lower for k in ['presentation', 'exam', 'viva', 'professor', 'grade', 'college', 'speech', 'interview', 'fail']):
        return (
            "I hear how agonizing that academic stress feels right now. When speaking in front of an audience or taking a crucial exam, "
            "our nervous system can perceive social evaluation as an existential threat, flooding your body with adrenaline. "
            "Please remember: stumbling in a presentation is a physiological hiccup, NOT a definition of your intellect or worth.\n\n"
            "**Immediate Soothing & Real-Life Cure:**\n"
            "1. **Physiological Sigh:** Take two quick inhales through your nose, then one long, slow exhale through your mouth. Do this 3 times to quickly lower heart rate.\n"
            "2. **Cognitive Reframe:** Most peers are so focused on their own evaluations that they rarely judge others harshly. One difficult moment does not undo years of your hard work.\n\n"
            "What is one small kindness you can offer yourself right now to unwind?"
        )
    elif any(k in t_lower for k in ['panic', 'cannot breathe', "can't breathe", 'heart racing', 'hyperventilate', 'shaking']):
        return (
            "I can sense the overwhelming intensity of that panic wave right now. Let's focus on grounding your nervous system together. "
            "Panic feels terrifying, but it cannot harm you; it is a temporary surge of adrenaline that will peak and subside.\n\n"
            "**Actionable Somatic Soothing (Right Now):**\n"
            "1. **Cold Water Reset:** Splash cold water on your cheeks or hold an ice cube. This triggers the mammalian dive reflex and physically forces your heart rate down.\n"
            "2. **5-4-3-2-1 Grounding:** Name out loud 5 things you can see, 4 things you can touch, 3 sounds you hear, 2 things you smell, and 1 taste.\n\n"
            "You are safe in this physical space. Place one hand on your chest and feel the breath slowing down."
        )
    elif any(k in t_lower for k in ['alone', 'lonely', 'nobody', 'no friends', 'ignored', 'left out', 'isolated']):
        return (
            "Feeling unseen and isolated can be one of the heaviest emotional spaces to inhabit. It is completely natural to crave meaningful connection, "
            "and when we feel alone, our minds often convince us that 'nobody cares'. That is the emotional fog speaking, not an absolute truth.\n\n"
            "**Real-Life Soothing & Connection Anchor:**\n"
            "1. **Sensory Comfort:** Wrap yourself in a warm blanket or hold a hot mug of tea. Physical warmth stimulates feelings of safety.\n"
            "2. **Low-Stakes Connection:** You don't need a deep heart-to-heart immediately. Saying hello to a neighbor, commenting in a hobby forum, or walking around outside gently reduces isolation.\n\n"
            "I am genuinely glad you are here talking with me today. What is something you normally enjoy doing when you have quiet time?"
        )
    elif p_class == "Suicidal" or analysis.get("risk_assessment", {}).get("is_crisis"):
        return (
            "I hear how exhausted and in unbearable pain you are feeling right now, and I want you to know with absolute certainty: your life has profound value. "
            "You do not have to carry this crushing weight alone.\n\n"
            "**Immediate Safety Action:**\n"
            "Please connect with trained, compassionate professionals who are ready to support you 24/7 without judgment:\n"
            "• **Tele-MANAS (Govt. of India):** Dial **14416** or **1800 891 4416** (Toll-Free, 20+ Languages)\n"
            "• **Vandrevala Foundation:** Call or WhatsApp **+91 9999 666 555**\n"
            "• **AASRA:** Call **+91 98204 66726**\n\n"
            "Take a breath and stay safe with me. Can you reach out to one of these helplines or someone in your home right now?"
        )
    elif p_class == "Depression":
        return (
            "Thank you for sharing your truth with me. Depression can make even the simplest actions—getting out of bed, replying to a message, eating—feel like scaling a mountain. "
            "Please be gentle with yourself. You are not lazy or broken; your brain's emotional batteries are depleted.\n\n"
            "**Gentle Micro-Interventions:**\n"
            "1. **Drop Demands:** Lower your expectations for today to the absolute baseline. If all you did was survive today, that is enough.\n"
            "2. **Micro-Movement:** Try opening one window for fresh air or sipping a glass of water. Just one tiny physical action.\n\n"
            "Have you been able to eat or rest today?"
        )
    else:
        return (
            f"I hear you, and thank you for reflecting with me. It takes real self-awareness to explore these thoughts. "
            f"Notice how your emotional state is currently showing {p_class.lower()} tendencies with {psychometrics.get('arousal_index')} activation. "
            "Remember that emotions are messengers, not permanent states. What is one supportive thing you can do for yourself in the next hour?"
        )


def generate_neural_mindbot_reply(messages: List[ChatMessage], analysis: dict, psychometrics: dict, custom_key: Optional[str] = None, user_name: str = "Friend") -> tuple:
    """Connects to live OpenRouter LLM Brain with fallback to dynamic situation-aware CBT engine."""
    api_key = custom_key or os.environ.get("OPENROUTER_API_KEY", "")
    latest_msg = messages[-1].content
    
    if not api_key:
        return generate_dynamic_cbt_fallback(latest_msg, analysis, psychometrics, user_name), "Dynamic CBT Intelligence Engine (Local)"
        
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://31232258arnav.github.io/MindGuard_AI/",
        "X-Title": "MindGuard AI Mental Health Platform"
    }
    
    system_prompt = (
        "You are MindGuard AI, an expert, compassionate clinical psychologist and mental health counselor. "
        "Your role is to provide authentic, highly empathetic active listening, situational validation, and "
        "concrete, evidence-based soothing/grounding techniques (CBT reframing, vagal nerve breathing, sensory resets, self-compassion). "
        "You have computed the following telemetry from the user's text:\n"
        f"- Target Affective State: {analysis.get('primary_class')} ({analysis.get('confidence_percentage')})\n"
        f"- Emotional Valence: {psychometrics.get('valence_score')} (range -1.0 to +1.0)\n"
        f"- Somatic Arousal: {psychometrics.get('arousal_index')}\n"
        f"- Cognitive Distortions: {', '.join(psychometrics.get('distortions_detected', []))}\n"
        f"- Prescribed Intervention: {psychometrics.get('prescribed_soothing')}\n\n"
        "GUIDELINES:\n"
        "1. NEVER use generic canned responses. Speak warmly, authentically, and conversationally.\n"
        "2. Directly address the user's specific scenario (college presentation, relationships, exams, family, fatigue, etc.).\n"
        "3. Explain their cognitive distortion gently and offer a real-life soothing exercise or cure.\n"
        "4. Format with clean, readable markdown (short paragraphs, bullet points for exercises).\n"
        "5. If there is explicit suicidal intent or severe self-harm, gently urge connecting with 24/7 helplines: "
        "Tele-MANAS (14416 / 1800 891 4416) or Vandrevala Foundation (+91 9999 666 555)."
    )
    
    formatted_messages = [{"role": "system", "content": system_prompt}]
    for m in messages[-6:]:
        formatted_messages.append({"role": m.role, "content": m.content})
        
    payload = {
        "model": "openrouter/free",
        "messages": formatted_messages,
        "temperature": 0.7,
        "max_tokens": 600
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=20)
        if res.status_code == 200:
            content = res.json()["choices"][0]["message"]["content"]
            return content, "OpenRouter Neural Brain (Live LLM)"
        else:
            return generate_dynamic_cbt_fallback(latest_msg, analysis, psychometrics, user_name), "Dynamic CBT Intelligence Engine (Fallback)"
    except Exception:
        return generate_dynamic_cbt_fallback(latest_msg, analysis, psychometrics, user_name), "Dynamic CBT Intelligence Engine (Fallback)"


@app.post("/api/chat")
def conversational_screening(req: ChatSessionRequest):
    """
    Conversational mental-health screening agent with live AI Brain & calculating power.
    Maintains dialogue context, computes cognitive distortions, and delivers real-life soothing.
    """
    if not req.messages:
        raise HTTPException(status_code=400, detail="No messages in chat session.")
    
    latest_msg = req.messages[-1].content
    analysis = predictor.predict(latest_msg)
    
    is_crisis = analysis["risk_assessment"]["is_crisis"]
    
    # Run Calculating Power Module
    psychometrics = calculate_psychometrics(latest_msg, req.messages)
    
    # Generate authentic AI Brain response
    bot_response, brain_source = generate_neural_mindbot_reply(
        req.messages, 
        analysis, 
        psychometrics, 
        custom_key=req.api_key, 
        user_name=req.user_name
    )
        
    return {
        "reply": bot_response,
        "ai_brain_source": brain_source,
        "message_analysis": analysis,
        "psychometrics": psychometrics,
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
