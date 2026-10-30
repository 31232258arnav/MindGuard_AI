"""
MindGuard AI - Server Launcher
Runs the FastAPI REST API and serves the interactive frontend on http://127.0.0.1:8000
"""

import uvicorn
import os
import sys

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    print("=" * 70)
    print("MINDGUARD AI: BERT-BASED MENTAL HEALTH SENTIMENTAL ANALYSIS")
    print("MindGuard AI Research Initiative Minor Project (2026-2027)")
    print("Authors: MindGuard Clinical AI Research Team")
    print("Mentor: Clinical NLP & Cognitive Systems Advisory Board")
    print("=" * 70)
    print("Starting server on http://127.0.0.1:8000 ...")
    uvicorn.run("backend.api:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
