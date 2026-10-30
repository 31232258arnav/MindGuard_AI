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
    print("Vishwakarma University Group 21 Minor Project (2026-2027)")
    print("Authors: Bhupesh Bhatia, Samruddhi Meher, Arnav Phuke, Sushrut Ingle, Saket Radke")
    print("Mentor: Prof. Richa Agnihotri")
    print("=" * 70)
    print("Starting server on http://127.0.0.1:8000 ...")
    uvicorn.run("backend.api:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
