"""
MindGuard AI - Colleague Presentation & Comprehensive Technical Report Generator
Generates a formal, hospital-grade and academic PDF document covering:
1. Master Links Directory (24/7 Web App, GitHub, Cloud Deployment, Endpoints, Crisis Helplines)
2. Technology Stack & Architectural Breakdown ("What is used")
3. Step-by-Step Guide on "How to Explain to Colleagues & Professors"
4. Paper Benchmarks & Empirical Tables (Table 1 to Table 4)
5. 24/7 Cloud & Offline In-Browser Hybrid Architecture
6. Ethical Boundaries & Clinical Triage Guardrails
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class ColleagueReportCanvas(canvas.Canvas):
    """
    Two-pass canvas for professional academic headers, running footers,
    and dynamic 'Page X of Y' numbering on all pages except the cover page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        if self._pageNumber == 1:
            return  # Suppress on cover page

        self.saveState()
        page_w, page_h = letter

        # Running Top Header
        self.setFont('Helvetica-Bold', 7.5)
        self.setFillColor(colors.HexColor('#0F172A'))
        self.drawString(54, page_h - 36, "MINDGUARD AI: CLINICAL SENTIMENTAL ANALYSIS PLATFORM")
        self.setFont('Helvetica', 7.5)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(320, page_h - 36, "|  Technical Colleague Briefing & Architecture Manual")
        self.drawRightString(page_w - 54, page_h - 36, "A.Y. 2026-2027")

        # Top Header Rule
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.6)
        self.line(54, page_h - 42, page_w - 54, page_h - 42)

        # Bottom Footer Rule
        self.setStrokeColor(colors.HexColor('#CBD5E1'))
        self.setLineWidth(0.6)
        self.line(54, 42, page_w - 54, 42)

        # Running Bottom Footer
        self.setFont('Helvetica', 7.5)
        self.setFillColor(colors.HexColor('#64748B'))
        self.drawString(54, 30, "Confidential Academic & Clinical Research Presentation Document  •  24/7 Cloud Architecture")
        self.setFont('Helvetica-Bold', 7.5)
        self.setFillColor(colors.HexColor('#0F172A'))
        self.drawRightString(page_w - 54, 30, f"Page {self._pageNumber} of {total_pages}")

        self.restoreState()


def build_colleague_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    c_primary = colors.HexColor('#0F172A')
    c_secondary = colors.HexColor('#1E293B')
    c_accent = colors.HexColor('#2563EB')
    c_success = colors.HexColor('#059669')
    c_warning = colors.HexColor('#D97706')
    c_danger = colors.HexColor('#DC2626')
    c_purple = colors.HexColor('#7C3AED')
    c_text = colors.HexColor('#1E293B')
    c_muted = colors.HexColor('#475569')
    c_bg_light = colors.HexColor('#F8FAFC')
    c_border = colors.HexColor('#E2E8F0')

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=c_primary,
        alignment=0,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11.5,
        leading=16,
        textColor=c_accent,
        spaceAfter=18
    )

    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=13,
        textColor=c_muted
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=c_text,
        spaceAfter=7
    )

    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12.5,
        textColor=c_primary
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=12,
        textColor=c_text,
        leftIndent=14,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=12,
        textColor=c_secondary
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#0F172A')
    )

    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.white,
        alignment=1
    )

    td_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10,
        textColor=c_text
    )

    td_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.6,
        leading=10,
        textColor=c_primary
    )

    td_center = ParagraphStyle(
        'TableCellCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10,
        textColor=c_text,
        alignment=1
    )

    story = []

    # ==================== COVER / TITLE HEADER ====================
    story.append(Spacer(1, 10))
    story.append(Paragraph("MINDGUARD AI", title_style))
    story.append(Paragraph("Sentimental Analysis for Early Mental Health Screening & Clinical Triage<br/><b>Comprehensive Colleague Presentation & Technical Architecture Briefing</b>", subtitle_style))

    # Meta Info Card
    meta_data = [
        [
            Paragraph("<b>Institution:</b> Department of Computer Engineering, Research Consortium", meta_style),
            Paragraph("<b>Target Domain:</b> Clinical NLP & Cognitive Systems", meta_style)
        ],
        [
            Paragraph("<b>Academic Year:</b> 2026-2027 | <b>Group No:</b> 21", meta_style),
            Paragraph("<b>Core Model:</b> Fine-Tuned BERT-base-uncased (110M params)", meta_style)
        ],
        [
            Paragraph("<b>Research Team:</b> Lead ML Engineer, Psychometric Specialist, Systems Architect", meta_style),
            Paragraph("<b>GenAI Model:</b> Clinical MindGuard GenAI (Google Gemini 2.5)", meta_style)
        ],
        [
            Paragraph("<b>Deployment Status:</b> Live 24/7 on GitHub Pages & Cloudflare Tunnel", meta_style),
            Paragraph("<b>Test Accuracy:</b> 83.00% (Weighted F1: 0.8299, 10,536 samples)", meta_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[270, 234])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # Executive Overview
    story.append(Paragraph("<b>Executive Summary:</b> MindGuard AI is a dual-engine mental health detection system built to identify emotional strain, depressive inertia, suicidal risk, chronic anxiety, stress, bipolar swings, and personality disorder patterns from textual discourse. It couples a fine-tuned, 110-million parameter BERT text classification model with a guarded, evidence-based GenAI clinical companion (MindGuard GenAI) and an autonomous in-browser processing architecture that guarantees 24/7 global availability without requiring local servers.", body_style))
    story.append(Spacer(1, 8))

    # ==================== SECTION 1: MASTER DIRECTORY OF ALL LINKS ====================
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=10))
    story.append(Paragraph("1. Master Directory of Live Platform Links", h1_style))
    story.append(Paragraph("Every operational URL for accessing the application, developer endpoints, cloud deployment repositories, and emergency mental health resources is cataloged below for your colleagues:", body_style))

    links_table_data = [
        [Paragraph("Category / Service", th_style), Paragraph("Destination URL & Access Details", th_style), Paragraph("Uptime & Scope", th_style)],
        [
            Paragraph("<b>Primary 24/7 Web App</b><br/>(GitHub Pages)", td_bold),
            Paragraph("<b>https://31232258arnav.github.io/MindGuard_AI/</b><br/>Live production frontend. Accessible globally on mobile, tablet, and desktop.", td_style),
            Paragraph("<font color='#059669'><b>24/7 Permanent</b></font><br/>Zero laptop dependence.", td_center)
        ],
        [
            Paragraph("<b>GitHub Code Repository</b>", td_bold),
            Paragraph("<b>https://github.com/31232258arnav/MindGuard_AI</b><br/>Full open source repository: model engine, FastAPI backend, clinical dataset, and paper reports.", td_style),
            Paragraph("<font color='#059669'><b>Public / Active</b></font><br/>Branch: <code>main</code>", td_center)
        ],
        [
            Paragraph("<b>GitHub Actions (CI/CD)</b>", td_bold),
            Paragraph("<b>https://github.com/31232258arnav/MindGuard_AI/actions</b><br/>Automated workflow monitoring for continuous GitHub Pages build and deployment.", td_style),
            Paragraph("<font color='#059669'><b>Continuous</b></font><br/>Auto-deploys on push", td_center)
        ],
        [
            Paragraph("<b>1-Click Render Cloud Deploy</b>", td_bold),
            Paragraph("<b>https://render.com/deploy?repo=https://github.com/31232258arnav/MindGuard_AI</b><br/>Provisions a dedicated 24/7 Python FastAPI cloud server using <code>render.yaml</code>.", td_style),
            Paragraph("<font color='#2563EB'><b>Free Cloud</b></font><br/>Zero manual setup", td_center)
        ],
        [
            Paragraph("<b>1-Click Vercel Deploy</b>", td_bold),
            Paragraph("<b>https://vercel.com/new/clone?repository-url=https://github.com/31232258arnav/MindGuard_AI</b><br/>Serverless deployment via <code>vercel.json</code> and <code>api/index.py</code>.", td_style),
            Paragraph("<font color='#2563EB'><b>Serverless</b></font><br/>Global edge network", td_center)
        ],
        [
            Paragraph("<b>Live Cloudflare Tunnel</b><br/>(Public HTTPS Proxy)", td_bold),
            Paragraph("<b>https://hollow-persian-pittsburgh-reality.trycloudflare.com</b><br/>Exposes the local FastAPI backend to the public web for remote screening & telemetry.", td_style),
            Paragraph("<font color='#D97706'><b>Live Session</b></font><br/>Active via daemon", td_center)
        ],
        [
            Paragraph("<b>Interactive Swagger UI</b><br/>(API Documentation)", td_bold),
            Paragraph("<b>http://127.0.0.1:8000/docs</b> (or <code>/docs</code> on the public tunnel)<br/>Complete OpenAPI 3.0 specification with interactive 'Try it out' request testing.", td_style),
            Paragraph("<font color='#7C3AED'><b>Developer API</b></font><br/>FastAPI Swagger", td_center)
        ],
        [
            Paragraph("<b>ReDoc API Documentation</b>", td_bold),
            Paragraph("<b>http://127.0.0.1:8000/redoc</b> (or <code>/redoc</code> on public tunnel)<br/>Structured technical REST reference describing payloads, headers, and schemas.", td_style),
            Paragraph("<font color='#7C3AED'><b>Developer API</b></font><br/>ReDoc Format", td_center)
        ],
        [
            Paragraph("<b>Tele-MANAS Helpline</b><br/>(Govt. of India)", td_bold),
            Paragraph("<b>14416 / 1800 891 4416</b>  •  https://telemanas.mohfw.gov.in/<br/>National 24/7 free mental health helpline in 20+ languages.", td_style),
            Paragraph("<font color='#DC2626'><b>24/7 Crisis SOS</b></font><br/>Toll-Free Pan-India", td_center)
        ],
        [
            Paragraph("<b>Vandrevala Foundation</b>", td_bold),
            Paragraph("<b>+91 9999 666 555</b>  •  https://www.vandrevalafoundation.com/<br/>24/7 free professional crisis counseling via voice call and WhatsApp.", td_style),
            Paragraph("<font color='#DC2626'><b>24/7 Crisis SOS</b></font><br/>Free Counseling", td_center)
        ],
        [
            Paragraph("<b>988 Crisis Lifeline</b><br/>(US / Canada)", td_bold),
            Paragraph("<b>988</b> (Call or Text)  •  https://988lifeline.org/<br/>Immediate confidential suicide and emotional crisis intervention.", td_style),
            Paragraph("<font color='#DC2626'><b>24/7 Crisis SOS</b></font><br/>North America", td_center)
        ]
    ]

    t_links = Table(links_table_data, colWidths=[115, 290, 99])
    t_links.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t_links)
    story.append(Spacer(1, 14))

    # ==================== SECTION 2: WHAT TECHNOLOGIES ARE USED ====================
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=10))
    story.append(Paragraph("2. Technical Stack Breakdown ('What Technologies Are Used')", h1_style))
    story.append(Paragraph("When presenting to colleagues or professors, use this section to explain the precise libraries, machine learning architectures, and infrastructure decisions:", body_style))

    tech_items = [
        ("1. BERT Fine-Tuned NLP Encoder (bert-base-uncased)",
         "A 12-layer, 768-hidden dimension bidirectional transformer with 12 self-attention heads and 110M parameters. It processes text through a WordPiece tokenizer (max length 128 tokens) and extracts pooled contextual [CLS] sentence representations. A Linear classification head with Dropout maps these representations to 7 clinical sentiment classes."),
        
        ("2. Calibrated 7-Class Inference Engine (backend/model_engine.py)",
         "Executes temperature-scaled Softmax (T=1.1) across the 7 categories: Normal, Depression, Suicidal, Anxiety, Stress, Bipolar, and Personality Disorder. Incorporates multi-word phrase matching, valence-inverting negation handling (e.g., 'not feeling good' correctly routes to Depression rather than falsely matching 'good'), and token saliency attribution."),

        ("3. FastAPI High-Throughput Microservice (backend/api.py)",
         "Asynchronous ASGI backend running on Uvicorn. Exposes REST endpoints for single-statement screening (<code>/api/analyze</code>), conversational check-in (<code>/api/chat</code>), bulk dataset processing (<code>/api/batch</code>), document analysis (<code>/api/analyze-file</code>), and clinical intake audit (<code>/api/clinical-file-audit</code>)."),

        ("4. MindGuard GenAI Engine with Mental Health Guardrails (backend/langchain_brain.py)",
         "Integrates Google Gemini 2.5 Flash via LangChain with strict mental health domain scoping. If a user asks off-topic queries (coding, trivia, sports), the model warmly declines and redirects them to their emotional well-being. Equipped with three clinical function tools: <code>screen_statement</code>, <code>get_evidence_based_coping_protocol</code>, and <code>lookup_crisis_helplines</code>. Anonymized to conceal backend engine identities."),

        ("5. Psychometric NLP Analytics & Cognitive Distortion Tracker",
         "Heuristic and neural detection of 6 common Cognitive Distortions: Catastrophizing, All-or-Nothing Thinking, Mind Reading, Personalization, Emotional Reasoning, and Inflexible 'Should' Demands. Simultaneously computes an Emotional Valence score (-1.0 to +1.0), Somatic Arousal Index (0% to 100%), and an Emotional Trajectory across multi-turn sessions."),

        ("6. Document & Multi-Format Clinical File Analyzer (backend/file_analyzer.py)",
         "Processes PDF (<code>pypdf</code>), Word DOCX (<code>python-docx</code>), CSV (<code>pandas</code>), and TXT notes. Sanitizes PII (emails, phone numbers, IPs) for HIPAA/GDPR compliance, extracts sentence boundaries, computes longitudinal sentiment trajectories, and auto-generates formal clinical SOAP Notes (Subjective, Objective, Assessment, Plan)."),

        ("7. 24/7 Autonomous Hybrid Cloud Architecture",
         "The frontend is hosted permanently on GitHub Pages. If the user's laptop is closed and local servers shut down, the browser seamlessly falls back to an embedded in-browser JavaScript clinical engine and direct HTTPS calls to the GenAI Cloud Engine. The site never shows blank errors or disconnects.")
    ]

    for title, desc in tech_items:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc, body_style))

    story.append(Spacer(1, 10))

    # ==================== SECTION 3: HOW TO EXPLAIN TO COLLEAGUES ====================
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=10))
    story.append(Paragraph("3. How to Explain MindGuard AI to Your Colleagues", h1_style))
    story.append(Paragraph("Use these scripted presentation talking points and live demonstration sequences during lab discussions, team meetings, or project viva presentations:", body_style))

    story.append(Paragraph("<b>A. The 30-Second Elevator Pitch:</b>", h2_style))
    story.append(Paragraph("<i>\"MindGuard AI is an early mental health screening platform that uses a fine-tuned BERT transformer to detect subtle psychological distress indicators across 7 clinical categories. Unlike generic chatbots, MindGuard AI provides calibrated probability distributions, highlights the exact words that triggered the prediction, automatically calculates clinical risk levels, and connects users in crisis directly to 24/7 helplines like Tele-MANAS. Furthermore, its hybrid cloud architecture allows it to run 24/7 directly from GitHub Pages without requiring a local laptop to stay powered on.\"</i>", callout_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>B. The 3-Minute Technical Architecture Walkthrough:</b>", h2_style))
    story.append(Paragraph("<b>1. Input Preprocessing:</b> Raw input text is stripped of URLs and punctuation artifacts, then tokenized using BERT's WordPiece vocabulary into maximum 128-token sequences.", bullet_style))
    story.append(Paragraph("<b>2. Transformer Encoding:</b> 12 transformer encoder layers generate self-attention matrices across all word pairs, capturing deep contextual relationships (such as distinguishing 'I am feeling sick of life' from 'I am feeling sick with a cold').", bullet_style))
    story.append(Paragraph("<b>3. Classification Head & Calibrated Logits:</b> The pooled [CLS] token is passed through a linear projection layer and evaluated with temperature scaling to prevent overconfidence, producing predictions across all 7 classes.", bullet_style))
    story.append(Paragraph("<b>4. Explainability & Risk Stratification:</b> Saliency attribution calculates which tokens contributed most heavily to the primary class. If Suicidal risk is detected or probability exceeds 25%, the system immediately triggers the Critical Crisis protocol.", bullet_style))
    story.append(Paragraph("<b>5. MindGuard GenAI Companion:</b> When users chat in MindBot, a specialized clinical prompt ensures responses remain compassionate, therapeutic, and strictly relevant to mental health, redirecting off-topic queries and providing real somatic coping exercises.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>C. Live Demo Guide for Colleagues (Step-by-Step):</b>", h2_style))
    demo_steps = [
        ("Step 1: Open the Live URL", "Navigate to <b>https://31232258arnav.github.io/MindGuard_AI/</b> on any device (laptop or smartphone). Show that the application loads instantly over HTTPS with zero installation required."),
        ("Step 2: Demonstrate Live Screener", "Click the 'Normal' sample button (e.g., 'Went for a morning run') ➔ Model predicts <b>Normal (99.9%)</b> with Low Risk badge. Next, enter a distressed statement (e.g., 'I have no energy and feel completely empty') ➔ Model immediately detects <b>Depression (100.0%)</b> with Elevated Clinical Strain badge and token saliency map."),
        ("Step 3: Trigger the Emergency Crisis Protocol", "Load the Suicidal sample ('I just want this pain to stop and kill myself') ➔ Watch the red <b>CRITICAL CRISIS EMERGENCY</b> banner appear instantly with direct one-click phone links to Tele-MANAS (14416) and Vandrevala Foundation."),
        ("Step 4: MindBot GenAI Guardrail Test", "Switch to the MindBot tab. First, ask an off-topic question: <i>'What is the capital of France?'</i> ➔ Show how MindGuard GenAI politely declines and steers the dialogue back to emotional well-being. Then ask: <i>'I am feeling panicky, my chest is tight'</i> ➔ Watch it guide the user through a structured 4-7-8 vagal breathing protocol."),
        ("Step 5: Batch CSV / Document Upload", "Switch to the Batch tab and drop in a dataset of patient statements. Demonstrate how it processes hundreds of statements simultaneously, plots the interactive Chart.js doughnut chart, and categorizes overall population risk.")
    ]
    for step_title, step_desc in demo_steps:
        story.append(Paragraph(f"• <b>{step_title}:</b> {step_desc}", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>D. How to Answer Tough Questions from Colleagues:</b>", h2_style))

    qa_items = [
        ("Q: Why did you use BERT instead of just prompting ChatGPT or Gemini for classification?",
         "<b>A:</b> Large LLMs are non-deterministic, expensive, latency-heavy (~2-4 seconds), and prone to hallucinated verdicts. BERT-base provides consistent, reproducible, mathematically calibrated probability distributions in under 50 milliseconds. BERT serves as the clinical classification engine, while GenAI serves as the conversational support companion."),
        
        ("Q: How does the system handle negations like 'I do not feel good'?",
         "<b>A:</b> Naive bag-of-words classifiers falsely match the word 'good' and classify it as Normal. MindGuard AI incorporates valence-inverting negation detection that identifies 'not', 'no', 'never', or 'can\\'t' preceding positive anchors, flipping the attribution to Depression with high confidence."),
        
        ("Q: What happens if the backend server goes down or my laptop turns off?",
         "<b>A:</b> The platform uses a resilient three-tier architecture: if the backend server is unreachable, the client-side JavaScript engine takes over immediately in the visitor's browser. It evaluates text against the calibrated clinical anchors and connects directly to the GenAI cloud endpoint over HTTPS with zero interruption.")
    ]
    for q, a in qa_items:
        story.append(Paragraph(f"<font color='#2563EB'><b>{q}</b></font>", body_bold))
        story.append(Paragraph(a, body_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))

    # ==================== SECTION 4: PAPER BENCHMARKS & TABLES ====================
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=10))
    story.append(Paragraph("4. Formal Research Benchmarks & Empirical Tables", h1_style))
    story.append(Paragraph("The exact experimental parameters and validation results from the research paper are presented below:", body_style))

    # Table 1: Dataset Distribution
    story.append(Paragraph("<b>Table I: Mental Health Benchmark Corpus Class Distribution (Test Set: 10,536 Samples)</b>", h2_style))
    t1_data = [
        [Paragraph("Category Name", th_style), Paragraph("Sample Count", th_style), Paragraph("Percentage Share", th_style), Paragraph("Clinical Manifestation", th_style)],
        [Paragraph("Normal", td_bold), Paragraph("3,269", td_center), Paragraph("31.02%", td_center), Paragraph("Healthy baseline, positive emotional valence, absence of acute distress.", td_style)],
        [Paragraph("Depression", td_bold), Paragraph("3,081", td_center), Paragraph("29.24%", td_center), Paragraph("Persistent sadness, loss of interest, anhedonia, fatigue, feelings of worthlessness.", td_style)],
        [Paragraph("Suicidal", td_bold), Paragraph("2,130", td_center), Paragraph("20.22%", td_center), Paragraph("Active/passive suicidal ideation, self-harm references, acute crisis indicators.", td_style)],
        [Paragraph("Anxiety", td_bold), Paragraph("768", td_center), Paragraph("7.29%", td_center), Paragraph("Panic symptoms, somatic palpitations, hypervigilance, excessive dread.", td_style)],
        [Paragraph("Bipolar", td_bold), Paragraph("555", td_center), Paragraph("5.27%", td_center), Paragraph("Manic episodes, insomnia without fatigue, grandiosity, affective cycling.", td_style)],
        [Paragraph("Stress", td_bold), Paragraph("518", td_center), Paragraph("4.92%", td_center), Paragraph("Academic pressure, occupational burnout, cognitive fatigue, headache.", td_style)],
        [Paragraph("Personality disorder", td_bold), Paragraph("215", td_center), Paragraph("2.04%", td_center), Paragraph("Fear of abandonment, emotional dysregulation, splitting, chronic emptiness.", td_style)],
        [Paragraph("<b>Total Test Set</b>", td_bold), Paragraph("<b>10,536</b>", td_center), Paragraph("<b>100.00%</b>", td_center), Paragraph("Stratified 20% split from 52,680 record Kaggle Mental Health corpus.", td_style)]
    ]
    t1 = Table(t1_data, colWidths=[100, 70, 80, 254])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, c_bg_light]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F1F5F9')),
    ]))
    story.append(t1)
    story.append(Spacer(1, 10))

    # Table 2: Model Configuration
    story.append(Paragraph("<b>Table II: BERT Fine-Tuning Hyperparameters & Execution Environment</b>", h2_style))
    t2_data = [
        [Paragraph("Hyperparameter / Setting", th_style), Paragraph("Engine Value", th_style), Paragraph("Clinical / Architectural Justification", th_style)],
        [Paragraph("Base Architecture", td_bold), Paragraph("bert-base-uncased", td_center), Paragraph("Pre-trained on BooksCorpus & English Wikipedia; 110M parameters.", td_style)],
        [Paragraph("Maximum Token Length", td_bold), Paragraph("128 tokens", td_center), Paragraph("Covers 98.4% of social media mental health posts without truncation.", td_style)],
        [Paragraph("Batch Size", td_bold), Paragraph("16", td_center), Paragraph("Optimal GPU memory utilization and gradient estimation stability.", td_style)],
        [Paragraph("Optimizer", td_bold), Paragraph("AdamW (eps = 1e-8)", td_center), Paragraph("Weight decay (0.01) regularizes against transformer parameter memorization.", td_style)],
        [Paragraph("Learning Rate", td_bold), Paragraph("2e-5 (Linear Decay)", td_center), Paragraph("Standard fine-tuning rate prevents catastrophic forgetting of language priors.", td_style)],
        [Paragraph("Warm-up Steps", td_bold), Paragraph("0", td_center), Paragraph("Constant decay schedule starting from initial learning rate.", td_style)],
        [Paragraph("Gradient Clipping", td_bold), Paragraph("Max Norm 1.0", td_center), Paragraph("Prevents exploding gradients during backpropagation through 12 layers.", td_style)],
        [Paragraph("Training Epochs", td_bold), Paragraph("7 Epochs", td_center), Paragraph("Validation loss monitored; Epoch 5 selected as optimal checkpoint.", td_style)],
        [Paragraph("Dataset Partition", td_bold), Paragraph("72% / 8% / 20%", td_center), Paragraph("Stratified split: 37,929 Train, 4,215 Validation, 10,536 Test.", td_style)]
    ]
    t2 = Table(t2_data, colWidths=[120, 100, 284])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(t2)
    story.append(Spacer(1, 10))

    # Table 3: Classification Report
    story.append(Paragraph("<b>Table III: Per-Class Precision, Recall, and F1-Scores on Independent Test Set (10,536 Records)</b>", h2_style))
    t3_data = [
        [Paragraph("Class Name", th_style), Paragraph("Precision", th_style), Paragraph("Recall", th_style), Paragraph("F1-Score", th_style), Paragraph("Support", th_style)],
        [Paragraph("Normal", td_bold), Paragraph("0.9576", td_center), Paragraph("0.9523", td_center), Paragraph("<b>0.9549</b>", td_center), Paragraph("3,269", td_center)],
        [Paragraph("Anxiety", td_bold), Paragraph("0.8753", td_center), Paragraph("0.8958", td_center), Paragraph("<b>0.8855</b>", td_center), Paragraph("768", td_center)],
        [Paragraph("Bipolar", td_bold), Paragraph("0.8330", td_center), Paragraph("0.8721", td_center), Paragraph("<b>0.8521</b>", td_center), Paragraph("555", td_center)],
        [Paragraph("Depression", td_bold), Paragraph("0.7712", td_center), Paragraph("0.7790", td_center), Paragraph("<b>0.7751</b>", td_center), Paragraph("3,081", td_center)],
        [Paragraph("Personality disorder", td_bold), Paragraph("0.8093", td_center), Paragraph("0.7302", td_center), Paragraph("<b>0.7677</b>", td_center), Paragraph("215", td_center)],
        [Paragraph("Stress", td_bold), Paragraph("0.7866", td_center), Paragraph("0.7471", td_center), Paragraph("<b>0.7663</b>", td_center), Paragraph("518", td_center)],
        [Paragraph("Suicidal", td_bold), Paragraph("0.7151", td_center), Paragraph("0.7117", td_center), Paragraph("<b>0.7134</b>", td_center), Paragraph("2,130", td_center)],
        [Paragraph("<b>Overall Accuracy</b>", td_bold), Paragraph("—", td_center), Paragraph("—", td_center), Paragraph("<b>0.8300 (83.00%)</b>", td_center), Paragraph("10,536", td_center)],
        [Paragraph("<b>Weighted Average</b>", td_bold), Paragraph("0.8301", td_center), Paragraph("0.8300", td_center), Paragraph("<b>0.8299</b>", td_center), Paragraph("10,536", td_center)],
        [Paragraph("<b>Macro Average</b>", td_bold), Paragraph("0.8212", td_center), Paragraph("0.8126", td_center), Paragraph("<b>0.8164</b>", td_center), Paragraph("10,536", td_center)]
    ]
    t3 = Table(t3_data, colWidths=[120, 95, 95, 100, 94])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-4), [colors.white, c_bg_light]),
        ('BACKGROUND', (0,-3), (-1,-1), colors.HexColor('#F1F5F9')),
    ]))
    story.append(t3)
    story.append(Spacer(1, 10))

    # Table 4: Epoch Dynamics
    story.append(Paragraph("<b>Table IV: Training Dynamics Across 7 Epochs (Validation Checkpoint at Epoch 5)</b>", h2_style))
    t4_data = [
        [Paragraph("Epoch", th_style), Paragraph("Train Loss", th_style), Paragraph("Train Acc", th_style), Paragraph("Val Loss", th_style), Paragraph("Val Acc", th_style), Paragraph("Val F1", th_style), Paragraph("Status / Checkpoint", th_style)],
        [Paragraph("Epoch 1", td_bold), Paragraph("0.8373", td_center), Paragraph("67.87%", td_center), Paragraph("0.5102", td_center), Paragraph("79.67%", td_center), Paragraph("0.7953", td_center), Paragraph("Rapid adaptation", td_style)],
        [Paragraph("Epoch 2", td_bold), Paragraph("0.4217", td_center), Paragraph("83.06%", td_center), Paragraph("0.4690", td_center), Paragraph("81.42%", td_center), Paragraph("0.8120", td_center), Paragraph("Substantial convergence", td_style)],
        [Paragraph("Epoch 3", td_bold), Paragraph("0.3006", td_center), Paragraph("87.84%", td_center), Paragraph("0.4737", td_center), Paragraph("82.68%", td_center), Paragraph("0.8267", td_center), Paragraph("High generalization", td_style)],
        [Paragraph("Epoch 4", td_bold), Paragraph("0.2093", td_center), Paragraph("92.23%", td_center), Paragraph("0.5842", td_center), Paragraph("81.97%", td_center), Paragraph("0.8156", td_center), Paragraph("Slight loss oscillation", td_style)],
        [Paragraph("<b>Epoch 5 (BEST)</b>", td_bold), Paragraph("<b>0.1379</b>", td_center), Paragraph("<b>95.49%</b>", td_center), Paragraph("<b>0.6844</b>", td_center), Paragraph("<b>82.80%</b>", td_center), Paragraph("<b>0.8278</b>", td_center), Paragraph("<font color='#059669'><b>Selected Checkpoint</b></font>", td_style)],
        [Paragraph("Epoch 6", td_bold), Paragraph("0.0887", td_center), Paragraph("97.49%", td_center), Paragraph("0.8731", td_center), Paragraph("82.66%", td_center), Paragraph("0.8263", td_center), Paragraph("Early overfitting onset", td_style)],
        [Paragraph("Epoch 7", td_bold), Paragraph("0.0579", td_center), Paragraph("98.45%", td_center), Paragraph("0.9394", td_center), Paragraph("82.63%", td_center), Paragraph("0.8264", td_center), Paragraph("Memorization detected", td_style)]
    ]
    t4 = Table(t4_data, colWidths=[65, 70, 70, 70, 70, 70, 89])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_secondary),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor('#ECFDF5')),  # Highlight Best Epoch 5
    ]))
    story.append(t4)
    story.append(Spacer(1, 14))

    # ==================== SECTION 5: ETHICAL SAFEGUARDS & CONCLUSION ====================
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=10))
    story.append(Paragraph("5. Ethical Boundaries, Privacy & Clinical Disclaimers", h1_style))
    story.append(Paragraph("<b>1. Clinical Scope Disclaimer:</b> MindGuard AI is an automated psychometric screening aid designed for early detection research. It is strictly non-diagnostic and does not replace consultation with a licensed psychiatrist, clinical psychologist, or medical provider.", bullet_style))
    story.append(Paragraph("<b>2. Automated Crisis Escalation:</b> Any statement matching acute suicidal ideation, intent, or self-harm triggers immediate high-priority emergency banner overrides. The system prioritizes immediate contact with Tele-MANAS (14416) and Vandrevala Foundation (+91 9999 666 555).", bullet_style))
    story.append(Paragraph("<b>3. Privacy & Sanitization:</b> All document uploads and text statements undergo regex sanitization stripping email addresses, 10-digit phone numbers, and IP addresses before model classification to ensure compliance with HIPAA and GDPR research ethics standards.", bullet_style))
    story.append(Spacer(1, 12))

    # Concluding Signature Block
    sign_block = [
        [
            Paragraph("<b>Report Generated & Certified by:</b><br/>Clinical AI Systems Engineering & Research Consortium", meta_style),
            Paragraph(f"<b>Publication Date:</b> October 2026<br/><b>Repository:</b> 31232258arnav/MindGuard_AI", meta_style)
        ]
    ]
    t_sign = Table(sign_block, colWidths=[300, 204])
    t_sign.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,-1), 1, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=ColleagueReportCanvas)
    print(f"Successfully generated PDF report at: {output_path}")


if __name__ == "__main__":
    output_pdf = os.path.join(os.path.dirname(__file__), "MindGuard_AI_Colleague_Presentation_Report.pdf")
    build_academic_pdf = build_colleague_pdf
    build_colleague_pdf(output_pdf)
