"""
MindGuard AI - Clinical Document & Multi-Format File Analyzer
 Vishwakarma University Group 21.

Accepts PDF, DOCX, CSV, and TXT files, extracts raw text, executes multi-level
sentence-by-sentence 7-class mental health classification, extracts cognitive distortions,
computes clinical triage boundaries, and generates structured clinical reports.
"""

import io
import os
import re
import math
from typing import Dict, Any, List, Optional
import pandas as pd
import pypdf
import docx

from backend.model_engine import predictor, CLASSES
from backend.langchain_brain import detect_heuristic_distortions, CRISIS_HELPLINES

def extract_file_content(file_bytes: bytes, filename: str) -> tuple[str, Dict[str, Any]]:
    """
    Extracts plain text from PDF, DOCX, CSV, or TXT file bytes.
    Returns (extracted_text, metadata).
    """
    ext = os.path.splitext(filename)[1].lower()
    text_parts = []
    meta = {
        "filename": filename,
        "extension": ext,
        "file_size_bytes": len(file_bytes),
        "pages_or_rows": 0
    }

    if ext == ".pdf":
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        meta["pages_or_rows"] = len(reader.pages)
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                text_parts.append(page_text.strip())
        full_text = "\n\n".join(text_parts)

    elif ext == ".docx":
        doc = docx.Document(io.BytesIO(file_bytes))
        meta["pages_or_rows"] = len(doc.paragraphs)
        for p in doc.paragraphs:
            if p.text.strip():
                text_parts.append(p.text.strip())
        for table in doc.tables:
            for row in table.rows:
                row_vals = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_vals:
                    text_parts.append(" | ".join(row_vals))
        full_text = "\n".join(text_parts)

    elif ext == ".csv":
        try:
            df = pd.read_csv(io.BytesIO(file_bytes))
        except Exception:
            df = pd.read_csv(io.BytesIO(file_bytes), encoding="latin-1")
            
        meta["pages_or_rows"] = len(df)
        
        # Look for text/statement/prompt/content columns
        text_cols = [c for c in df.columns if any(k in c.lower() for k in ["text", "statement", "prompt", "msg", "message", "content", "utterance", "review", "sentence"])]
        if not text_cols:
            text_cols = [c for c in df.columns if df[c].dtype == object]
            
        if text_cols:
            for col in text_cols[:3]:
                col_texts = df[col].dropna().astype(str).tolist()
                text_parts.extend(col_texts[:200]) # Cap at 200 rows for swift responsiveness
        else:
            text_parts.append(df.to_string())
            
        full_text = "\n".join(text_parts)

    else: # TXT or plain text
        try:
            full_text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            full_text = file_bytes.decode("latin-1", errors="replace")
        meta["pages_or_rows"] = full_text.count("\n") + 1

    return full_text.strip(), meta


def split_into_sentences(text: str) -> List[str]:
    """Splits text into meaningful sentences/statements for classification."""
    raw_sentences = re.split(r"(?<=[.!?\n])\s+", text)
    clean_sentences = []
    for s in raw_sentences:
        s_clean = s.strip()
        # Keep sentences with at least 3 words and under 500 characters
        if len(s_clean.split()) >= 3 and len(s_clean) <= 500:
            clean_sentences.append(s_clean)
    return clean_sentences


def analyze_document_mental_health(
    file_bytes: bytes,
    filename: str,
    max_sentences: int = 50
) -> Dict[str, Any]:
    """
    Performs full multi-level mental health analysis of an uploaded document.
    """
    raw_text, meta = extract_file_content(file_bytes, filename)
    
    if not raw_text:
        return {
            "error": "No readable textual content could be extracted from this file.",
            "metadata": meta
        }

    words = raw_text.split()
    total_words = len(words)
    total_chars = len(raw_text)
    
    sentences = split_into_sentences(raw_text)
    total_sentences = len(sentences)
    
    # Sample sentences evenly if document is large
    sample_pool = sentences
    if len(sentences) > max_sentences:
        step = max(1, len(sentences) // max_sentences)
        sample_pool = sentences[::step][:max_sentences]

    # Run 7-class prediction on each sampled sentence
    class_counts = {c: 0 for c in CLASSES}
    high_risk_statements = []
    sentence_records = []
    
    total_sampled = max(1, len(sample_pool))
    
    for s in sample_pool:
        pred = predictor.predict(s)
        p_class = pred["primary_class"]
        class_counts[p_class] += 1
        
        is_crisis = p_class == "Suicidal" or pred.get("risk_assessment", {}).get("is_crisis", False)
        
        rec = {
            "sentence": s[:180] + ("..." if len(s) > 180 else ""),
            "primary_class": p_class,
            "confidence": pred["confidence_percentage"],
            "is_crisis": is_crisis
        }
        sentence_records.append(rec)
        
        if is_crisis or p_class in ["Suicidal", "Depression", "Anxiety"] and float(pred["confidence_percentage"].replace("%", "")) > 70:
            high_risk_statements.append({
                "quote": s[:200],
                "class": p_class,
                "confidence": pred["confidence_percentage"],
                "reason": "Elevated clinical concern detected" if not is_crisis else "Critical crisis intervention marker"
            })

    # Class percentages
    class_shares = {c: round((class_counts[c] / total_sampled) * 100, 1) for c in CLASSES}
    
    # Dominant class across document
    dominant_class = max(class_shares.items(), key=lambda x: x[1])[0]
    
    # Document-wide cognitive distortions
    distortions = detect_heuristic_distortions(raw_text[:4000])
    
    # Determine Clinical Boundary for Document
    suicidal_count = class_counts.get("Suicidal", 0)
    depression_count = class_counts.get("Depression", 0)
    anxiety_count = class_counts.get("Anxiety", 0)
    
    if suicidal_count > 0:
        triage_level = "Acute Crisis Risk"
        boundary_statement = "CRITICAL BOUNDARY TRIGGER: Explicit or severe crisis markers detected in document content."
        action_recommendation = "Immediate professional crisis intervention required. Provide direct crisis helpline contact."
        has_crisis = True
    elif class_shares.get("Depression", 0) + class_shares.get("Anxiety", 0) >= 40:
        triage_level = "Moderate Clinical Strain"
        boundary_statement = "Elevated clinical distress profile across document. Screening aid only (Non-Diagnostic)."
        action_recommendation = "Consultation with a licensed clinical psychologist or academic counselor recommended."
        has_crisis = False
    elif class_shares.get("Stress", 0) + class_shares.get("Anxiety", 0) >= 30:
        triage_level = "Mild Concern"
        boundary_statement = "Situational stress and academic/occupational pressure detected in document."
        action_recommendation = "Engage somatic grounding, balanced workload scheduling, and mindfulness exercises."
        has_crisis = False
    else:
        triage_level = "Safe / Baseline"
        boundary_statement = "Document exhibits normative emotional cadence with balanced psychological markers."
        action_recommendation = "Continue healthy mental self-care, reflection, and balanced cognitive habits."
        has_crisis = False

    # Document Executive Summary Synthesis
    summary_text = (
        f"MindGuard AI Document Audit for '{filename}': Evaluated {total_words} words across {total_sentences} sentences. "
        f"The primary affective orientation of this document is '{dominant_class}' ({class_shares.get(dominant_class, 0)}% of content). "
        f"Overall Clinical Triage Status: [{triage_level}]. "
        f"{'CRITICAL WARNING: ' + str(suicidal_count) + ' statement(s) exhibited crisis-level markers. Emergency resources attached.' if has_crisis else 'No acute crisis markers identified.'}"
    )

    return {
        "status": "success",
        "file_info": {
            "filename": filename,
            "extension": meta["extension"],
            "file_size_kb": round(meta["file_size_bytes"] / 1024, 1),
            "total_words": total_words,
            "total_sentences": total_sentences,
            "analyzed_sentences": len(sample_pool)
        },
        "clinical_boundary": {
            "triage_level": triage_level,
            "scope_statement": boundary_statement,
            "mandatory_action": action_recommendation,
            "crisis_triggered": has_crisis,
            "helplines": CRISIS_HELPLINES if has_crisis or triage_level in ["Acute Crisis Risk", "Moderate Clinical Strain"] else []
        },
        "affective_profile": {
            "dominant_class": dominant_class,
            "class_distribution_percent": class_shares,
            "class_counts": class_counts
        },
        "cognitive_distortions_found": distortions,
        "high_risk_statements": high_risk_statements[:6],
        "sample_sentences_analyzed": sentence_records[:15],
        "executive_summary": summary_text
    }
