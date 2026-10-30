"""
MindGuard AI Public Tunnel Launcher
Launches Cloudflare Tunnel to expose the local MindGuard AI server to a public HTTPS URL.
"""

import subprocess
import time
import re
import sys
import os

cloudflared_path = r"C:\Program Files (x86)\cloudflared\cloudflared.exe"

print("=" * 60)
print("[*] Launching MindGuard AI Cloudflare Public Tunnel...")
print("=" * 60)

cf_proc = subprocess.Popen(
    [cloudflared_path, "tunnel", "--url", "http://127.0.0.1:8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    encoding="utf-8",
    errors="replace"
)

public_url = None
start_time = time.time()

while time.time() - start_time < 35:
    line = cf_proc.stdout.readline()
    if not line:
        continue
    # Look for trycloudflare.com URL
    match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
    if match:
        public_url = match.group(0)
        break

if public_url:
    print(f"\n[SUCCESS] MindGuard AI is LIVE globally!")
    print("=" * 60)
    print(f"Public HTTPS URL: {public_url}")
    print(f"Local URL:        http://127.0.0.1:8000")
    print("=" * 60)
    
    with open("active_url.txt", "w", encoding="utf-8") as f:
        f.write(public_url)
        
    # Keep tunnel running
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        cf_proc.terminate()
else:
    print("[ERROR] Could not extract public Cloudflare URL within timeout.")
