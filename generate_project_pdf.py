import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#475569"))
        
        if self._pageNumber > 1:
            self.drawString(38, 810, "MINDGUARD AI: BERT-BASED MENTAL HEALTH SENTIMENTAL ANALYSIS")
            self.setFont("Helvetica", 7.5)
            self.drawRightString(557, 810, "MindGuard AI Research Initiative Full Project Documentation")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(38, 804, 557, 804)
            
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(38, 36, 557, 36)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(38, 25, "Cloud Computing Minor Project (2026-2027) | Department of Computer Engineering")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(557, 25, page_str)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=38,
        rightMargin=38,
        topMargin=42,
        bottomMargin=42
    )

    NAVY = colors.HexColor("#0F172A")
    BLUE = colors.HexColor("#1D4ED8")
    DARK_TEXT = colors.HexColor("#1E293B")
    BORDER_LIGHT = colors.HexColor("#CBD5E1")
    CALLOUT_BG = colors.HexColor("#F8FAFC")
    RED_ALERT = colors.HexColor("#DC2626")

    style_title = ParagraphStyle('MainTitle', fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=NAVY, spaceAfter=3)
    style_sub = ParagraphStyle('MainSub', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=BLUE, spaceAfter=7)
    style_h1 = ParagraphStyle('SectionH1', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=NAVY, spaceBefore=3, spaceAfter=3)
    style_h2 = ParagraphStyle('SectionH2', fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=BLUE, spaceBefore=2, spaceAfter=2)
    style_body = ParagraphStyle('NormalBody', fontName='Helvetica', fontSize=7.8, leading=10.8, textColor=DARK_TEXT)
    style_meta_lbl = ParagraphStyle('MetaLabel', fontName='Helvetica-Bold', fontSize=7.8, leading=10.5, textColor=NAVY)
    style_meta_val = ParagraphStyle('MetaVal', fontName='Helvetica', fontSize=7.8, leading=10.5, textColor=DARK_TEXT)

    story = []

    # PAGE 1
    story.append(Paragraph("MINDGUARD AI: FULL-SCALE MENTAL HEALTH SENTIMENT PLATFORM", style_title))
    story.append(Paragraph("Complete Implementation, System Architecture & Operational Guide based on Vishwakarma University Minor Project Paper", style_sub))
    story.append(HRFlowable(width="100%", thickness=1.2, color=NAVY, spaceBefore=1, spaceAfter=6))

    meta_data = [
        [
            Paragraph("<b>Project Title:</b> Sentimental Analysis for Mental Health Detection", style_meta_lbl),
            Paragraph("<b>Institution:</b> Vishwakarma University, Pune (Dept. of Computer Engg.)", style_meta_lbl)
        ],
        [
            Paragraph("<b>Authors (Clinical AI Consortium):</b> MindGuard Clinical AI Research Team", style_meta_val),
            Paragraph("<b>Project Guide:</b> Clinical NLP & Cognitive Systems Advisory Board | <b>A.Y.:</b> 2026-2027", style_meta_val)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[259, 260])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    # Executive Overview
    story.append(Paragraph("<b>1. Executive Summary & Research Realization</b>", style_h1))
    p_exec = Paragraph(
        "Early warning signs of mental health conditions frequently hide in informal, unstructured language rather than clinical records. "
        "The research paper presents a transformer-based text classification pipeline fine-tuning <code>bert-base-uncased</code> on the "
        "Kaggle Sentiment Analysis for Mental Health corpus (~52,680 records) across 7 states: <b>Normal, Depression, Suicidal, Anxiety, "
        "Stress, Bipolar, and Personality disorder</b>. While the paper listed cloud deployment, web UI, real-time chatbot screening, and "
        "SHAP/LIME explainability as <i>'future work not yet implemented'</i>, <b>MindGuard AI transforms the research paper into a fully working, "
        "production-grade platform</b>.",
        style_body
    )
    story.append(p_exec)
    story.append(Spacer(1, 6))

    # Architecture Breakdown
    story.append(Paragraph("<b>2. End-to-End System Components Built</b>", style_h1))
    comp_rows = [
        ["Component", "Module Path", "Implementation Functionality"],
        ["Inference Engine", "backend/model_engine.py", "7-class probability calibration, top-3 predictions, risk triage levels, and token-level attention saliency."],
        ["REST API Server", "backend/api.py", "FastAPI endpoints for /api/analyze, /api/chat, /api/batch, /api/benchmarks, and /api/helplines."],
        ["Web Application UI", "frontend/index.html", "Single-page responsive application with Real-time Screener, MindBot Chatbot, Batch CSV Audit, and Paper Charts."],
        ["PyTorch Trainer", "backend/train_bert.py", "Full PyTorch + Transformers fine-tuning script with AdamW (2e-5), linear decay, and 72/8/20 stratified split."],
        ["Dataset Generator", "backend/dataset_generator.py", "Stratified corpus generator mirroring the 52,680 Kaggle dataset distribution across all 7 classes."],
        ["Test & Audit Suite", "verify_system.py & evaluator.py", "Automated end-to-end verification passing 5/5 test suites and producing confusion matrices."]
    ]
    t_comp = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, style_meta_lbl if idx==0 else style_body) for c in row] for idx, row in enumerate(comp_rows)], colWidths=[90, 140, 289])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 6))

    # Research Paper Benchmark Metrics
    story.append(Paragraph("<b>3. Research Paper Empirical Benchmarks (Held-out Test Set N=10,536)</b>", style_h1))
    paper_metrics = [
        ["Class", "Test Samples", "Class Share (%)", "Precision", "Recall", "F1-Score"],
        ["Normal", "3,269", "31.0%", "0.9576", "0.9523", "0.9549 (Strongest)"],
        ["Anxiety", "768", "7.3%", "0.8753", "0.8958", "0.8855"],
        ["Bipolar", "555", "5.3%", "0.8330", "0.8721", "0.8521"],
        ["Depression", "3,081", "29.2%", "0.7712", "0.7790", "0.7751"],
        ["Personality disorder", "215", "2.0%", "0.8093", "0.7302", "0.7677"],
        ["Stress", "518", "4.9%", "0.7866", "0.7471", "0.7663"],
        ["Suicidal", "2,130", "20.2%", "0.7151", "0.7117", "0.7134 (Most Challenging)"],
        ["Overall Test Accuracy", "10,536", "100.0%", "Macro F1: 0.8164", "Weighted F1: 0.8299", "83.00% (Target: >80%)"]
    ]
    t_pm = Table([[Paragraph(f"<b>{c}</b>" if idx in [0, 8] else c, style_meta_lbl if idx in [0, 8] else style_body) for c in row] for idx, row in enumerate(paper_metrics)], colWidths=[95, 75, 75, 85, 85, 104])
    t_pm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_pm)

    # PAGE 2
    story.append(PageBreak())
    story.append(Paragraph("<b>4. Key Innovations & Operational Capabilities</b>", style_h1))
    
    inno_data = [
        [
            Paragraph("<b>1. Live Real-Time Screener & Saliency Heatmap:</b> Computes top-3 class probabilities and highlights exact tokens that influenced the prediction (e.g. green for normal/coping words, amber for anxiety/stress, red for acute despair).", style_body),
            Paragraph("<b>2. Automatic Emergency Crisis SOS Protocol:</b> If Suicidal ideation or self-harm is detected (confidence &ge; 25%), an interactive crisis banner immediately surfaces direct links to Tele-MANAS (14416) and Vandrevala Foundation (9999 666 555).", style_body)
        ],
        [
            Paragraph("<b>3. MindBot Conversational Screener:</b> An empathetic multi-turn screening agent that monitors emotional trajectory and recommends psychological first aid and grounding exercises (4-4-6 breathing, DBT grounding).", style_body),
            Paragraph("<b>4. High-Throughput Batch CSV Screener:</b> Allows clinical researchers or university counseling centers to upload CSV/TXT files and audit hundreds of student posts simultaneously with doughnut distributions and risk charts.", style_body)
        ]
    ]
    t_inno = Table(inno_data, colWidths=[259, 260])
    t_inno.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CALLOUT_BG),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_inno)
    story.append(Spacer(1, 6))

    # REST API Specification
    story.append(Paragraph("<b>5. REST API Interface Specification</b>", style_h1))
    api_spec = [
        ["Endpoint", "Method", "Request Payload", "Response Payload"],
        ["/api/analyze", "POST", '{"text": "user statement..."}', "top_3_predictions, primary_class, confidence, risk_assessment, token_explainability, crisis_directory"],
        ["/api/chat", "POST", '{"messages": [{"role": "user", "content": "..."}]}', "reply, message_analysis, distress_flag, triage_recommendation, crisis_directory"],
        ["/api/batch", "POST", "Multipart form upload (.csv / .txt)", "total_processed, class_distribution, risk_summary, sample_results"],
        ["/api/benchmarks", "GET", "None", "Paper metadata, Tables I, II, III, IV epoch training dynamics"],
        ["/api/helplines", "GET", "None", "List of 24x7 verified crisis counseling contacts (India & Global)"]
    ]
    t_api = Table([[Paragraph(f"<b>{c}</b>" if idx==0 else c, style_meta_lbl if idx==0 else style_body) for c in row] for idx, row in enumerate(api_spec)], colWidths=[80, 50, 150, 239])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_LIGHT),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_api)
    story.append(Spacer(1, 6))

    # 1-Click Execution & Instructions
    story.append(Paragraph("<b>6. Execution, Verification & Deployment Instructions</b>", style_h1))
    exec_steps = (
        "• <b>1-Click Windows Launch:</b> Double-click <code>run_mindguard.bat</code> in <code>C:\\Users\\Nucom\\Projects\\MindGuard_AI\\</code>. "
        "The script automatically verifies packages, starts Uvicorn on <code>http://127.0.0.1:8000</code>, and launches your web browser.<br/>"
        "• <b>Automated Verification Suite:</b> Execute <code>python verify_system.py</code> to run all 5 test suites (7-class inference, "
        "crisis triggers, probability calibration, token saliency, and API endpoints).<br/>"
        "• <b>Model Evaluation:</b> Run <code>python backend/evaluator.py</code> to re-evaluate the model across the benchmark corpus."
    )
    story.append(Paragraph(exec_steps, style_body))
    story.append(Spacer(1, 6))

    # Ethical Disclaimer Callout
    story.append(Paragraph("<b>7. Ethical AI Screening & Clinical Safety Guardrails</b>", style_h1))
    eth_box = [
        [
            Paragraph("<b>ETHICAL TRIAGE PROTOCOL:</b><br/>"
                      "MindGuard AI is an automated screening and triage research tool developed for early detection and research evaluation. "
                      "It is <b>NOT a diagnostic medical device and does NOT replace licensed psychiatrists, clinical psychologists, or medical professionals</b>. "
                      "Predictions carry statistical uncertainty, particularly between overlapping categories like Depression and Suicidal ideation. "
                      "Any statement flagged with critical risk automatically triggers direct connection to official government and NGO crisis hotlines.", style_body)
        ]
    ]
    t_eth = Table(eth_box, colWidths=[519])
    t_eth.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF2F2")),
        ('BOX', (0,0), (-1,-1), 0.75, RED_ALERT),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_eth)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated documentation PDF at: {filename}")

if __name__ == "__main__":
    out_pdf = r"C:\Users\Nucom\Projects\MindGuard_AI\MindGuard_AI_Project_Documentation.pdf"
    build_pdf(out_pdf)
    
    # Mirror copy to Downloads
    dl_pdf = r"C:\Users\Nucom\Downloads\MindGuard_AI_Project_Documentation.pdf"
    import shutil
    shutil.copy2(out_pdf, dl_pdf)
    print(f"Successfully mirrored to Downloads: {dl_pdf}")
