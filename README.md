# MindGuard AI: Sentimental Analysis for Mental Health Detection

A full-scale, production-ready BERT-based text classification and early mental-health screening platform based on the research paper and presentation poster from **Vishwakarma University, Pune (Department of Computer Engineering, Clinical AI Consortium, A.Y. 2026-2027)**.

---

## Academic Project Details
* **Project Title:** Sentimental Analysis for Mental Health Detection (A BERT-based text classification system for early mental-health screening)
* **Institution:** Vishwakarma University, Pune — Faculty of Science and Technology, Department of Computer Engineering
* **Division:** Research Division | **Group Number:** 21
* **Project Guide / Mentor:** Clinical NLP & Cognitive Systems Advisory Board
* **Authors & Student Researchers:**
  1. **Lead ML Engineer** (Roll No: RES-2026-02)
  2. **Psychometric Research Specialist** (Roll No: RES-2026-03)
  3. **Core System Architect** (Roll No: RES-2026-01)
  4. **Backend Systems Engineer** (Roll No: RES-2026-04)
  5. **Clinical UI Specialist** (Roll No: RES-2026-05)

---

## 1. System Architecture & Processing Pipeline

```
+-------------------------------------------------------------------------------------------------+
|                               MINDGUARD AI SYSTEM ARCHITECTURE                                  |
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|   [ Kaggle Corpus (~52,680 Statements) ]                                                        |
|                 │                                                                               |
|                 ▼                                                                               |
|   [ Preprocessing & Cleaning ] ──► LabelEncoder ──► Stratified Split (72% Train, 8% Val, 20% Test)
|                 │                                                                               |
|                 ▼                                                                               |
|   [ WordPiece Tokenizer ] ──► [CLS] [SEP] tokens, Max Length 128, Attention Masks               |
|                 │                                                                               |
|                 ▼                                                                               |
|   [ BERT-base-uncased Encoder ] ──► 12 layers, 768 hidden, 12 attention heads, 110M params       |
|                 │                                                                               |
|                 ▼                                                                               |
|   [ Classification Head ] ──► Dropout + Linear Layer + Softmax (K = 7 Classes)                  |
|                 │                                                                               |
|                 ▼                                                                               |
|   [ Model Inference Engine ]                                                                    |
|                 ├──────────────┬────────────────────────┬────────────────────────┐              |
|                 ▼              ▼                        ▼                        ▼              |
|         Top-3 Predictions  Confidence Score     SHAP/Saliency Heatmap   Crisis SOS Emergency    |
|                 │              │                        │                        │              |
|                 ▼              ▼                        ▼                        ▼              |
|     [ REST API (FastAPI) ] ◄───┴────────────────────────┴────────────────────────┘              |
|                 │                                                                               |
|                 ▼                                                                               |
|     [ Web UI & Chatbot ] ──► Live Screener, MindBot Companion, Batch Audit & Paper Benchmarks   |
|                                                                                                 |
+-------------------------------------------------------------------------------------------------+
```

---

## 2. The 7 Mental Health Classes

| # | Mental Health State | Linguistic Focus | Severity / Risk Tier |
| :-: | :--- | :--- | :--- |
| **1** | **Normal** | Everyday pleasant, neutral, or constructive statements | **Low / Safe** |
| **2** | **Depression** | Emptiness, chronic numbness, loss of motivation/joy | **Elevated Risk** |
| **3** | **Suicidal** | Self-harm ideation, suicide notes, unbearable agony | **CRITICAL / CRISIS EMERGENCY** |
| **4** | **Anxiety** | Racing heart, panic attacks, dread, hypervigilance | **Mild / Distress Monitoring** |
| **5** | **Stress** | Overlapping deadlines, burnout, cognitive overload | **Mild / Distress Monitoring** |
| **6** | **Bipolar** | Swings between manic euphoria and severe depressive slumps | **Elevated Risk** |
| **7** | **Personality disorder** | Splitting, fear of abandonment, emotional dysregulation | **Elevated Risk** |

---

## 3. Empirical Research Benchmarks (From Paper Tables)

### Table I: Class Distribution in the Test Set (10,536 Samples)
* **Normal:** 3,269 (31.0%)
* **Depression:** 3,081 (29.2%)
* **Suicidal:** 2,130 (20.2%)
* **Anxiety:** 768 (7.3%)
* **Bipolar:** 555 (5.3%)
* **Stress:** 518 (4.9%)
* **Personality disorder:** 215 (2.0%)

### Table II: Training Configuration
* **Pre-trained Model:** `bert-base-uncased` (110M parameters)
* **Max Sequence Length:** 128 tokens
* **Batch Size:** 16
* **Optimizer:** AdamW ($\epsilon = 10^{-8}$)
* **Learning Rate:** $2 \times 10^{-5}$ with linear decay
* **Warm-up Steps:** 0 | **Gradient Clipping:** Max norm 1.0
* **Epochs:** 7 (Best Checkpoint selected at Epoch 5)

### Table III: Per-Class Classification Report
| Class | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
| **Normal** | 0.9576 | 0.9523 | **0.9549** | 3,269 |
| **Anxiety** | 0.8753 | 0.8958 | **0.8855** | 768 |
| **Bipolar** | 0.8330 | 0.8721 | **0.8521** | 555 |
| **Depression** | 0.7712 | 0.7790 | **0.7751** | 3,081 |
| **Personality disorder** | 0.8093 | 0.7302 | **0.7677** | 215 |
| **Stress** | 0.7866 | 0.7471 | **0.7663** | 518 |
| **Suicidal** | 0.7151 | 0.7117 | **0.7134** | 2,130 |
| **Overall Accuracy** | — | — | **0.8300 (83.00%)** | 10,536 |
| **Weighted Average** | 0.8301 | 0.8300 | **0.8299** | 10,536 |
| **Macro Average** | 0.8212 | 0.8126 | **0.8164** | 10,536 |

### Table IV: Training Dynamics Across 7 Epochs
* **Epoch 1:** Train Loss 0.8373, Train Acc 67.87% | Val Loss 0.5102, Val Acc 79.67%
* **Epoch 2:** Train Loss 0.4217, Train Acc 83.06% | Val Loss 0.4690, Val Acc 81.42%
* **Epoch 3:** Train Loss 0.3006, Train Acc 87.84% | Val Loss 0.4737, Val Acc 82.68%
* **Epoch 4:** Train Loss 0.2093, Train Acc 92.23% | Val Loss 0.5842, Val Acc 81.97%
* **Epoch 5 (BEST):** Train Loss 0.1379, Train Acc 95.49% | Val Loss 0.6844, Val Acc **82.80%** (Checkpoint Saved)
* **Epoch 6:** Train Loss 0.0887, Train Acc 97.49% | Val Loss 0.8731, Val Acc 82.66% (Overfitting)
* **Epoch 7:** Train Loss 0.0579, Train Acc 98.45% | Val Loss 0.9394, Val Acc 82.63% (Overfitting)

---

## 4. Key Platform Features

1. **Live Statement Screener:**
   - Real-time text classification with top-3 predictions and calibrated probabilities.
   - Dynamic Risk Triage categorization (Safe, Mild, Elevated, Critical).
   - **Emergency Crisis Banner & SOS Protocol:** Immediate 1-click trigger to Tele-MANAS (14416) and Vandrevala Foundation (9999 666 555) when suicidal ideation is detected.
   - **Token Saliency & Explainability Map:** Color-coded token attribution highlighting which words triggered anxiety, depression, or positive feelings.
2. **Conversational Screening Chatbot (MindBot):**
   - Empathetic conversational agent that conducts naturalistic mental health check-ins.
   - Tracks session emotional trajectory and alerts users if distress patterns escalate.
3. **Batch CSV / TXT Dataset Audit:**
   - Drag-and-drop file upload for processing hundreds of user posts simultaneously.
   - Generates interactive doughnut distribution charts and risk stratification bars.
4. **Research Benchmarks Interactive Dashboard:**
   - Visual charts of Epoch 1–7 loss curves and per-class F1 comparisons using Chart.js.
5. **Crisis Helpline Directory:**
   - 24/7 verified national and international mental health support contacts.

---

## 5. Quick Start Instructions

### 1-Click Launch (Windows)
Double-click [`run_mindguard.bat`](file:///C:/Users/Nucom/Projects/MindGuard_AI/run_mindguard.bat) to launch the server and open the web application automatically on `http://127.0.0.1:8000`.

### Manual CLI Launch
```powershell
cd C:\Users\Nucom\Projects\MindGuard_AI
python server.py
```
Open your browser to: **`http://127.0.0.1:8000`**

### Running the System Verification Suite
```powershell
cd C:\Users\Nucom\Projects\MindGuard_AI
python verify_system.py
```

### Running Model Corpus Evaluation
```powershell
cd C:\Users\Nucom\Projects\MindGuard_AI
python backend/evaluator.py
```

---

## 6. REST API Endpoints

* **`POST /api/analyze`**: Classify a single statement (returns top-3 classes, confidence, risk level, token explainability, crisis helplines).
* **`POST /api/chat`**: Conversational agent endpoint with sentiment trajectory tracking.
* **`POST /api/batch`**: Bulk CSV/TXT upload and multi-record sentiment audit.
* **`GET /api/benchmarks`**: Returns exact research paper experimental results, authors, and tables.
* **`GET /api/helplines`**: Returns verified 24/7 mental health emergency resources.
* **`GET /api/health`**: Health status and model metadata.

---

## 7. Ethical & Clinical Triage Disclaimer
*MindGuard AI is an automated screening and triage research tool developed for early detection and research evaluation. It is NOT a diagnostic medical device and does NOT replace licensed psychiatrists, clinical psychologists, or medical professionals. Statements indicating immediate risk of self-harm automatically trigger emergency crisis resources.*
