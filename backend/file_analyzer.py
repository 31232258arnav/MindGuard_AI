"""
MindGuard AI - Clinical Document & Multi-Format File Analyzer
MindGuard Clinical AI Research Consortium.

Accepts PDF, DOCX, CSV, and TXT files, executes PII sanitization, multi-level
sentence-by-sentence 7-class mental health classification, extracts cognitive distortions,
computes affective trajectories / emotional heatmaps, and synthesizes clinical SOAP notes.
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

def sanitize_pii(text: str) -> str:
    """
    HIPAA & GDPR clinical privacy guardrail.
    Sanitizes personal identifiable information (emails, phone numbers, IP addresses).
    """
    if not text:
        return ""
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]', text)
    text = re.sub(r'(\+?\d{1,3}[-.\s]?)?(?:\d{5}[-.\s]?\d{5}|\d{4}[-.\s]?\d{6}|\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b)', '[PHONE_REDACTED]', text)
    text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP_REDACTED]', text)
    return text

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
        text_cols = [c for c in df.columns if any(k in c.lower() for k in ["text", "statement", "prompt", "msg", "message", "content", "utterance", "review", "sentence"])]
        if not text_cols:
            text_cols = [c for c in df.columns if df[c].dtype == object]
            
        if text_cols:
            for col in text_cols[:3]:
                col_texts = df[col].dropna().astype(str).tolist()
                text_parts.extend(col_texts[:200])
        else:
            text_parts.append(df.to_string())
            
        full_text = "\n".join(text_parts)

    else:
        try:
            full_text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            full_text = file_bytes.decode("latin-1", errors="replace")
        meta["pages_or_rows"] = full_text.count("\n") + 1

    clean_text = sanitize_pii(full_text.strip())
    return clean_text, meta

def split_into_sentences(text: str) -> List[str]:
    """Splits text into meaningful sentences/statements for classification."""
    raw_sentences = re.split(r"(?<=[.!?\n])\s+", text)
    clean_sentences = []
    for s in raw_sentences:
        s_clean = s.strip()
        if len(s_clean.split()) >= 3 and len(s_clean) <= 500:
            clean_sentences.append(s_clean)
    return clean_sentences

def compute_affective_trajectory(sentences: List[str], window_size: int = 5) -> List[Dict[str, Any]]:
    """
    Computes a longitudinal affective trajectory / sentiment heatmap across document windows.
    """
    if not sentences:
        return []
        
    num_windows = max(1, math.ceil(len(sentences) / window_size))
    trajectory = []
    
    for w in range(num_windows):
        start = w * window_size
        chunk = sentences[start:start + window_size]
        if not chunk:
            continue
            
        # Sample predictions in chunk
        chunk_classes = {}
        for s in chunk:
            pred = predictor.predict(s)
            c = pred["primary_class"]
            chunk_classes[c] = chunk_classes.get(c, 0) + 1
            
        dom_class = max(chunk_classes.items(), key=lambda x: x[1])[0]
        
        # Calculate valence estimate
        neg_classes = {"Depression": -0.8, "Suicidal": -1.0, "Anxiety": -0.5, "Stress": -0.4, "Personality disorder": -0.6, "Bipolar": -0.5, "Normal": 0.4}
        avg_valence = round(sum(neg_classes.get(c, 0) * count for c, count in chunk_classes.items()) / len(chunk), 2)
        
        trajectory.append({
            "segment_index": w + 1,
            "sample_snippet": chunk[0][:80] + ("..." if len(chunk[0]) > 80 else ""),
            "dominant_class": dom_class,
            "valence_score": avg_valence,
            "sentence_count": len(chunk)
        })
        
    return trajectory

def generate_soap_note(
    filename: str,
    total_words: int,
    dominant_class: str,
    triage_level: str,
    class_shares: Dict[str, float],
    high_risks: List[Dict[str, Any]],
    distortions: List[Dict[str, str]],
    is_crisis: bool
) -> str:
    """
    Generates a formal, hospital-grade clinical SOAP Note (Subjective, Objective, Assessment, Plan).
    """
    # Subjective
    subjective_quotes = []
    for r in high_risks[:3]:
        subjective_quotes.append(f'  - Patient expressed: "{r.get("quote", "")}" (Classified as {r.get("class")})')
    if not subjective_quotes:
        subjective_quotes.append('  - Patient records reflect normative emotional self-reporting without acute crisis markers.')
    s_block = "\n".join(subjective_quotes)

    # Objective
    o_block = (
        f"  - Document Name: {filename}\n"
        f"  - Total Words Analyzed: {total_words}\n"
        f"  - Primary Affective Class: {dominant_class} ({class_shares.get(dominant_class, 0)}% of content)\n"
        f"  - 7-Class Distribution: " + ", ".join([f"{c}: {pct}%" for c, pct in class_shares.items() if pct > 0]) + "\n"
        f"  - Acute Risk Markers Detected: {len(high_risks)} elevated statements"
    )

    # Assessment
    d_names = [d.get("type", "Contextual Stress") for d in distortions[:3]]
    a_block = (
        f"  - Clinical Triage Tier: [{triage_level}]\n"
        f"  - Dominant Cognitive Distortions: {', '.join(d_names)}\n"
        f"  - Diagnostic Impression: Screening indicative of {dominant_class.lower()} tendencies. "
        f"{'CRITICAL WARNING: Imminent crisis protocol active.' if is_crisis else 'Sub-acute/moderate symptom profile observed.'}"
    )

    # Plan
    if is_crisis:
        p_block = (
            "  1. IMMEDIATE CRISIS MOBILIZATION: Connect patient with 24/7 emergency helplines:\n"
            "     - Tele-MANAS (Govt. of India): 14416 / 1800 891 4416\n"
            "     - Vandrevala Foundation: +91 9999 666 555\n"
            "  2. Remove access to lethal means and secure immediate in-person social or medical supervision.\n"
            "  3. Conduct full clinical psychiatric intake within 24 hours."
        )
    elif triage_level == "Moderate Clinical Strain":
        p_block = (
            "  1. Outpatient Behavioral Health Referral: Recommend clinical psychologist consultation.\n"
            "  2. Cognitive Restructuring: Initiate CBT thought record exercises addressing " + d_names[0] + ".\n"
            "  3. Somatic Regulation: Prescribe daily 4-7-8 vagal nerve breathing and sleep hygiene stabilization.\n"
            "  4. Re-evaluate using PHQ-9 & GAD-7 within 14 days."
        )
    else:
        p_block = (
            "  1. Psychoeducation: Reinforce positive coping mechanisms and mindfulness routines.\n"
            "  2. Lifestyle & Grounding: Box breathing (4-4-4-4) during situational pressure.\n"
            "  3. As-needed clinical re-screening if symptoms escalate."
        )

    soap = f"""================================================================================
MINDGUARD AI - CLINICAL SCREENING & TRIAGE SOAP NOTE
Confidential Healthcare Documentation - Automated Screening Protocol (Non-Diagnostic)
================================================================================
DATE: 2026-10-30 | FILE: {filename} | TRIAGE STATUS: {triage_level.upper()}

[S] SUBJECTIVE (Client Expressed Experience & Chief Complaint):
{s_block}

[O] OBJECTIVE (BERT 7-Class Quantified Diagnostics & Saliency):
{o_block}

[A] ASSESSMENT (Clinical Triage & Psychometric Impression):
{a_block}

[P] PLAN (Interventions, Grounding Protocols & Crisis Escalation):
{p_block}

================================================================================
DISCLAIMER: MindGuard AI is an automated clinical decision-support and screening aid.
It does not constitute formal psychiatric diagnosis. For emergency support, call 14416.
================================================================================"""
    return soap

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
    sentences = split_into_sentences(raw_text)
    total_sentences = len(sentences)
    
    sample_pool = sentences
    if len(sentences) > max_sentences:
        step = max(1, len(sentences) // max_sentences)
        sample_pool = sentences[::step][:max_sentences]

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
        
        if is_crisis or (p_class in ["Suicidal", "Depression", "Anxiety"] and float(pred["confidence_percentage"].replace("%", "")) > 70):
            high_risk_statements.append({
                "quote": s[:200],
                "class": p_class,
                "confidence": pred["confidence_percentage"],
                "reason": "Elevated clinical concern detected" if not is_crisis else "Critical crisis intervention marker"
            })

    class_shares = {c: round((class_counts[c] / total_sampled) * 100, 1) for c in CLASSES}
    dominant_class = max(class_shares.items(), key=lambda x: x[1])[0]
    distortions = detect_heuristic_distortions(raw_text[:4000])
    
    suicidal_count = class_counts.get("Suicidal", 0)
    has_crisis = suicidal_count > 0

    if has_crisis:
        triage_level = "Acute Crisis Risk"
        boundary_statement = "CRITICAL BOUNDARY TRIGGER: Explicit or severe crisis markers detected in document content."
        action_recommendation = "Immediate professional crisis intervention required. Connect with Tele-MANAS (14416)."
    elif class_shares.get("Depression", 0) + class_shares.get("Anxiety", 0) >= 40:
        triage_level = "Moderate Clinical Strain"
        boundary_statement = "Elevated clinical distress profile across document. Screening aid only (Non-Diagnostic)."
        action_recommendation = "Consultation with a licensed clinical psychologist or academic counselor recommended."
    elif class_shares.get("Stress", 0) + class_shares.get("Anxiety", 0) >= 30:
        triage_level = "Mild Concern"
        boundary_statement = "Situational stress and academic/occupational pressure detected in document."
        action_recommendation = "Engage somatic grounding, balanced workload scheduling, and mindfulness exercises."
    else:
        triage_level = "Safe / Baseline"
        boundary_statement = "Document exhibits normative emotional cadence with balanced psychological markers."
        action_recommendation = "Continue healthy mental self-care, reflection, and balanced cognitive habits."

    # Longitudinal Affective Trajectory
    trajectory = compute_affective_trajectory(sentences, window_size=max(2, len(sentences) // 8))

    # Formal SOAP Note
    soap_note = generate_soap_note(
        filename=filename,
        total_words=total_words,
        dominant_class=dominant_class,
        triage_level=triage_level,
        class_shares=class_shares,
        high_risks=high_risk_statements,
        distortions=distortions,
        is_crisis=has_crisis
    )

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
        "affective_trajectory": trajectory,
        "soap_note": soap_note,
        "cognitive_distortions_found": distortions,
        "high_risk_statements": high_risk_statements[:6],
        "sample_sentences_analyzed": sentence_records[:15],
        "executive_summary": summary_text
    }
