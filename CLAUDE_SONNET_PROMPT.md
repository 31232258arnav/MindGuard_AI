# MASTER PROMPT: MINDGUARD AI FULL-SCALE CLINICAL PRODUCTION ARCHITECTURE
### Designed for: Claude 3.5 Sonnet / Claude 3.7 / Sonnet 5.5 (Free & Pro Tiers)
---

> **INSTRUCTIONS FOR USER:**
> 1. Copy the entire contents of this prompt below.
> 2. Paste it into Claude AI (claude.ai) on Claude Sonnet.
> 3. Once Claude finishes generating the response, copy Claude's answer and save it into a file (for example: `C:\Users\Nucom\Downloads\claude_response.md` or `claude_instructions.txt`).
> 4. Return to Antigravity and simply tell me the path to the file (e.g., *"I saved Claude's response in C:\Users\Nucom\Downloads\claude_response.md, please execute it"*).
> 5. Antigravity will autonomously parse Claude's code, execute all upgrades, test the system, and deploy it live!

---

```markdown
# MISSION BRIEFING: MINDGUARD AI ENTERPRISE CLINICAL ARCHITECTURE & FULL-SCALE HARDENING

You are an Elite Principal AI Architect, Clinical Informatics Specialist, and Senior Full-Stack Engineer. You are conducting an exhaustive, production-grade architectural upgrade for **MindGuard AI**—a clinical-grade, BERT- and LangChain-powered Mental Health Sentimental Analysis, Early Screening, and Clinical Triage Platform.

All student names, personal identities, roll numbers, and professor references have been strictly anonymized. The system represents the **MindGuard Clinical AI Research Consortium**.

---

## 1. CURRENT SYSTEM STATE & REPOSITORY ARCHITECTURE

The platform is fully functional, deployed on GitHub Pages with a FastAPI backend tunneled over Cloudflare, featuring 9 live modules:

### Current Tech Stack:
- **Backend:** FastAPI (Python 3.14), Uvicorn, LangChain (`langchain_openai`, `langchain_core`), Pydantic v2.
- **Classification Engine:** 7-Class BERT-based text classifier (`bert-base-uncased` fine-tuned on 10,536 clinical samples with 82.80% validation accuracy and 0.8278 macro F1 score).
  - Classes: `Normal`, `Depression`, `Suicidal`, `Anxiety`, `Stress`, `Bipolar`, `Personality disorder`.
- **Multi-Format Document Analyzer:** Native support for `.pdf` (`pypdf`), `.docx` (`python-docx`), `.csv` (`pandas`), and `.txt`.
- **MindBot AI Brain:** Multi-tiered reasoning pipeline combining high-throughput LangChain models with an instant (<5ms) dynamic clinical psychometrics synthesizer. Returns structured JSON:
  - `clinical_boundary`: Triage level (`Safe / Baseline`, `Mild Concern`, `Moderate Clinical Strain`, `Acute Crisis Risk`), non-diagnostic scope notice, crisis triggers.
  - `affective_state`: Primary class, confidence %, somatic agitation level (0-100%).
  - `cognitive_distortions`: Beckian distortion detection with quotes & reframes.
  - `prescribed_soothing`: Evidence-based somatic protocols (Physiological Sigh, Vagal Reset, 5-4-3-2-1 Grounding).
  - `curative_reframe`: Cognitive restructuring insight and 1-hour micro-action.
  - `dialogue_response`: Warm, active-listening counseling dialogue.
  - `suggested_followups`: Dynamic, clickable chip prompts.
- **Frontend:** Responsive Single-Page Application (HTML5, Modern CSS3 Dark Theme `#06090E`, Vanilla ES6+ JavaScript, Zero bloated frameworks).
- **Public Endpoints:**
  - `GET  /api/health`
  - `POST /api/analyze` (single statement classification)
  - `POST /api/chat` (structured conversational triage)
  - `POST /api/analyze-file` (multipart upload for PDF, DOCX, CSV, TXT)
  - `POST /api/batch` (high-throughput CSV screening)
  - `GET  /api/benchmarks` (model validation tables)
  - `GET  /api/helplines` (24x7 verified crisis services: Tele-MANAS, Vandrevala, AASRA, KIRAN, 988)

---

## 2. THE OBJECTIVE: FULL-SCALE ENTERPRISE & CLINICAL HARDENING

We need your expert intelligence to provide complete, production-ready code upgrades and architectural enhancements across four vital pillars.

### PILLAR 1: Real-Time Token Streaming (Server-Sent Events / SSE)
Currently, `POST /api/chat` returns a complete JSON payload after generation.
- Design an asynchronous **Streaming Endpoint (`POST /api/chat/stream`)** using Server-Sent Events (SSE).
- Enable real-time typewriter-style rendering for MindBot, streaming the dialogue tokens smoothly while emitting the structured clinical boundary, somatic score, and soothing cards as structured SSE event frames (`event: metadata`, `event: token`, `event: cards`, `event: done`).
- Provide the exact FastAPI Python implementation and the matching Vanilla JavaScript frontend handler with full reconnection resilience.

### PILLAR 2: HIPAA / GDPR Privacy Guardrails & Client-Side PII Scrubbing
Mental health platforms must protect user privacy before text ever leaves the browser:
- Build a robust **Client-Side & Server-Side PII Sanitization Engine**:
  - Automatically detect and scrub: full human names, phone numbers, email addresses, dates of birth, physical addresses, IP addresses, and institutional identifiers.
  - Replace them with semantic clinical tokens (e.g. `[PATIENT_NAME]`, `[CONTACT_PHONE]`, `[INSTITUTION]`) so that psychometric classification remains 100% intact while maintaining zero PII leakage.

### PILLAR 3: DSM-5 / ICD-11 Aligned Clinical Triage & SOAP Note Generation
Upgrade the clinical boundary engine to hospital/clinic standards:
- **Four-Tier Triage Matrix:**
  1. *Level 1 - Baseline / Resilient:* Normative stress, healthy emotional regulation.
  2. *Level 2 - Mild Situational Distress:* Adjustment reactions, academic/occupational strain, transient sleep disturbances.
  3. *Level 3 - Moderate Clinical Strain:* Persistent depressive dysphoria, chronic anxiety, panic disorder symptoms, suspected cyclothymia/bipolar phases.
  4. *Level 4 - Acute Crisis Intervention:* Active or passive suicidal ideation, explicit self-harm intent, command hallucinations, or acute psychomotor agitation.
- **Automated Clinical SOAP Note Generator:**
  - Create a function in `backend/file_analyzer.py` and `backend/api.py` that automatically synthesizes a formal **SOAP Note** (Subjective, Objective, Assessment, Plan) from either a chat transcript or an uploaded document (PDF/DOCX/CSV/TXT), ready for clinical handoff or one-click PDF/TXT export.

### PILLAR 4: Multi-Page Longitudinal Document Analytics & Affective Heatmaps
Uploaded documents (such as diary entries, therapy transcripts, or research datasets) often span days or weeks:
- Implement a **Document Affective Heatmap & Temporal Trajectory Algorithm**:
  - Break down documents into sequential narrative windows (e.g. 100-word sliding windows or paragraph chunks).
  - Compute a rolling valence-arousal trajectory (`Valence`, `Arousal`, `Dominant Class`).
  - Return time-series data points that the frontend can render as a visual emotional trajectory curve or heatmap, showing exactly where emotional distress escalated or stabilized.

---

## 3. STRICT RESPONSE FORMAT REQUIREMENTS FOR CLAUDE

To ensure the AI coding assistant (Antigravity) can seamlessly execute your instructions with 0 errors:
1. Provide **complete, unabridged code files**. Do not use placeholders like `// ... rest of code remains the same ...` or `# TODO: implement this`.
2. Clearly specify the target relative file path for each component:
   - `backend/api.py`
   - `backend/langchain_brain.py`
   - `backend/file_analyzer.py`
   - `index.html` (and `frontend/index.html`)
3. Ensure all Python code is 100% compatible with Python 3.14, FastAPI, LangChain 1.4+, Pydantic v2, `pypdf`, `python-docx`, and `pandas`.
4. Ensure all frontend code is clean, robust Vanilla JavaScript (ES6+), compatible with modern evergreen browsers, with complete error handling in `try...catch...finally` blocks.
5. Maintain the anonymized branding: **MindGuard Clinical AI Research Consortium**.

Proceed with the complete, master-level architectural blueprint and drop-in code!
```
