# MindGuard AI — Clinical NLP Sentiment & Early Mental-Health Screening Platform

A full-scale, production-ready BERT-based text classification and early mental-health screening platform based on the research paper and presentation poster from **Vishwakarma University, Pune (Department of Computer Engineering, Division B, A.Y. 2026-2027)**.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/31232258arnav/MindGuard_AI)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/31232258arnav/MindGuard_AI)

- **24/7 Live Web Application (GitHub Pages):** [https://31232258arnav.github.io/MindGuard_AI/](https://31232258arnav.github.io/MindGuard_AI/)
- **Permanent Cloud Backend Service:** [https://render.com/deploy?repo=https://github.com/31232258arnav/MindGuard_AI](https://render.com/deploy?repo=https://github.com/31232258arnav/MindGuard_AI)
- **Live Interactive API Docs (Swagger):** `http://localhost:8000/docs` (or Render cloud `/docs`)
- **Automated Continuous Deployment Workflow:** [https://github.com/31232258arnav/MindGuard_AI/actions](https://github.com/31232258arnav/MindGuard_AI/actions)

---

## Academic Project Details
* **Project Title:** Sentimental Analysis for Mental Health Detection (A BERT-based text classification system for early mental-health screening)
* **Institution:** Vishwakarma University, Pune — Faculty of Science and Technology, Department of Computer Engineering
* **Division:** B | **Group Number:** 21
* **Project Guide / Mentor:** Professor Richa Agnihotri
* **Authors & Student Researchers:**
  1. **Arnav Phuke**
  2. **Sushrut Ingle**
  3. **Bhupesh Bhatia**
  4. **Saket Radke**
  5. **Samruddhi Meher**

---

## 1. System Architecture & Processing Pipeline

```
+-------------------------------------------------------------------------------------------------+
|                               MINDGUARD AI SYSTEM ARCHITECTURE                                  |
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|   +-----------------------------------------------------------------------------------------+   |
|   |                   USER CLIENT (Web Browser / Smartphone / Terminal)                     |   |
|   +-----------------------------------------------------------------------------------------+   |
|                                                |                                                |
|                      +-------------------------+-------------------------+                      |
|                      |                                                   |                      |
|                      v (HTTPS / REST)                                    v                      |
|       +------------------------------+                       +-----------------------+          |
|       |   PRODUCTION FASTAPI ASGI    |                       |   CLIENT-SIDE ZERO-   |          |
|       |   (Python Uvicorn Service)   |                       |   DEPENDENCY ENGINE   |          |
|       +------------------------------+                       |   (Regex + Lexicon)   |          |
|                      |                                       +-----------------------+          |
|       +--------------+--------------+                                    |                      |
|       |                             |                                    |                      |
|       v                             v                                    | (Fallback Mode)      |
|  +------------------------+   +-------------------------------+          |                      |
|  |  BERT ENCODER PIPELINE |   |   GEMINI NEURAL REASONER      |          |                      |
|  |  - PyTorch 2.0+        |   |   - Generative Clinical Brain |          |                      |
|  |  - 110M Transformer    |   |   - MindBot Persona Guard     |          |                      |
|  |  - 7 Target Classes    |   |   - Crisis Helpline Injection |          |                      |
|  +------------------------+   +-------------------------------+          |                      |
|               |                             |                            |                      |
|               +--------------+--------------+                            |                      |
|                              |                                           |                      |
|                              v                                           |                      |
|            +-----------------------------------+                         |                      |
|            |    DYNAMIC RISK & CRISIS TRIAGE   |<------------------------+                      |
|            +-----------------------------------+                                                |
|                              |                                                                  |
|             +----------------+----------------+                                                 |
|             v                                 v                                                 |
|   +-------------------+             +-------------------+                                       |
|   |  Standard Patient |             | Critical Distress |                                       |
|   |  Dashboard & SOAP |             | Immediate Helpline|                                       |
|   +-------------------+             +-------------------+                                       |
+-------------------------------------------------------------------------------------------------+
```

---

## 2. Dataset Distribution & Model Benchmark Metrics

Our model is trained and evaluated on **~52,680 text statements** compiled from standardized clinical screening corpora and psychological research records:

### Table I: Target Class Distribution & Test Metrics

| Class Index | Target Affective Class | Sample Count | Support Share | Test Precision | Test Recall | Test F1-Score | Clinical Risk Level |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | **Normal** | 3,269 | 31.02% | 0.9412 | 0.9691 | **0.9549** | Normal / Safe Baseline |
| **1** | **Depression** | 3,081 | 29.24% | 0.7712 | 0.7790 | **0.7751** | Elevated Clinical Strain |
| **2** | **Suicidal** | 2,130 | 20.22% | 0.7151 | 0.7117 | **0.7134** | **CRITICAL CRISIS ESCALATION** |
| **3** | **Anxiety** | 768 | 7.29% | 0.8753 | 0.8958 | **0.8855** | Mild Distress Monitoring |
| **4** | **Bipolar** | 555 | 5.27% | 0.8330 | 0.8721 | **0.8521** | Elevated Clinical Strain |
| **5** | **Stress** | 518 | 4.92% | 0.7866 | 0.7471 | **0.7663** | Situational Strain Monitoring |
| **6** | **Personality disorder** | 215 | 2.04% | 0.8093 | 0.7302 | **0.7677** | Moderate / Regulation Needed |
| — | **Overall Test Accuracy** | **10,536** | **100%** | — | — | **83.00%** | Macro F1: **0.8164** |
| — | **Weighted F1-Score** | **10,536** | **100%** | **0.8301** | **0.8300** | **0.8299** | Latency: **~142 ms** |

---

## 3. Core Capabilities & Clinical Modules

1. **Multi-Class Affective Classification:**
   - Real-time classification into 7 distinct mental health states using fine-tuned BERT embeddings.
   - Per-token explainability showing positive and negative attention saliency weights.

2. **Automated Psychometric Assessments:**
   - **PHQ-9 (Patient Health Questionnaire-9):** Clinical standard for major depression screening (Scores 0–27).
   - **GAD-7 (Generalized Anxiety Disorder-7):** Clinical standard for anxiety assessment (Scores 0–21).
   - Dynamic clinical interpretations matching DSM-5 criteria.

3. **Conversational Neural Chat (MindBot):**
   - Empathetic conversational agent strictly constrained to mental health and psychometric support.
   - Built-in multi-provider LLM brain (Google Gemini 2.5 Flash, OpenRouter Claude 3.5 Sonnet, DeepSeek V3, OpenAI GPT-4o-mini).
   - Instant emergency crisis protocol triggering localized national helplines for suicidal or severe self-harm ideation.

4. **Multi-Format Document Clinical Auditing:**
   - Supports direct upload and longitudinal sentiment trajectory scanning for **PDF, DOCX, CSV, and TXT** records.
   - Automated SOAP note generation (Subjective, Objective, Assessment, Plan).

5. **24/7 High-Availability Deployment Architecture:**
   - Static client-side Single Page Application (SPA) on **GitHub Pages** with zero runtime hosting costs.
   - Automated cloud backend blueprints for **Render** (`render.yaml`) and **Vercel** (`vercel.json`).
   - Resilient hybrid fallback topology guaranteeing seamless operation even during cloud cold starts or offline states.

---

## 4. Official Academic PDF Reports (In Repository)

The project includes four complete, publication-grade academic PDF reports located directly in the root directory:

1. **`MindGuard_AI_Comprehensive_Academic_Report.pdf`** (16 Pages)
   - Comprehensive university academic monograph including IEEE-format literature review, transformer mathematical formulations, 7-class confusion matrices, and clinical deployment ethics.
2. **`MindGuard_AI_Computer_Engineering_Architecture_Report.pdf`** (4 Pages)
   - Deep technical engineering architecture whitepaper covering distributed client/server topology, memory footprints, and OpenAPI 3.0 specs.
3. **`MindGuard_AI_Colleague_Presentation_Report.pdf`** (6 Pages)
   - Comprehensive executive walk-through and presentation guide designed for peer reviews, project viva, and colleague onboarding.
4. **`MindGuard_AI_Project_Documentation.pdf`** (2 Pages)
   - Summary technical documentation and operational overview.

---

## 5. Local Setup & Quickstart

### Prerequisites
- Python 3.10+
- PyTorch (optional for deep GPU inference; fallback engine is zero-dependency)

### Installation
```bash
# Clone the repository
git clone https://github.com/31232258arnav/MindGuard_AI.git
cd MindGuard_AI

# Install dependencies
pip install fastapi uvicorn pydantic requests pypdf python-docx reportlab

# Launch full server
python server.py
```
Open [http://localhost:8000](http://localhost:8000) in your browser to access the complete application.

---

## 6. License & Academic Disclaimer
Distributed under the MIT License for educational and research purposes. **MindGuard AI is a clinical decision-support and screening research prototype and does not replace certified professional medical diagnosis or clinical treatment.** In cases of acute psychiatric distress, immediately contact national crisis helplines (e.g., Tele-MANAS: 14416 / 1800-891-4416).
