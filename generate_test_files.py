import os
import csv

downloads_dir = r"C:\Users\Nucom\Downloads"
project_dir = r"C:\Users\Nucom\Projects\MindGuard_AI"

# 1. Comprehensive Test CSV Dataset for Batch Screener & Live Inference
csv_records = [
    {"id": 1, "statement": "I had a massive panic attack during my presentation and my heart was pounding so hard I felt like I was choking.", "expected_class": "Anxiety", "risk_level": "ELEVATED"},
    {"id": 2, "statement": "I feel like a complete and utter failure, nothing I do matters anymore and I have been crying in bed for days.", "expected_class": "Depression", "risk_level": "MODERATE"},
    {"id": 3, "statement": "I am so exhausted of this agonizing pain, I wrote my final goodbye letters and I just want to end it all tonight.", "expected_class": "Suicidal", "risk_level": "CRITICAL EMERGENCY"},
    {"id": 4, "statement": "Just finished my evening run with friends, feeling calm, happy, and looking forward to our weekend road trip!", "expected_class": "Normal", "risk_level": "NORMAL / SAFE"},
    {"id": 5, "statement": "Drowning under five engineering project deadlines this week with zero sleep, my brain is completely overwhelmed and fried.", "expected_class": "Stress", "risk_level": "MILD / ELEVATED"},
    {"id": 6, "statement": "Yesterday I had endless mania and cleaned my whole apartment at 3 AM with 10 business ideas, but today I crash into deep emptiness.", "expected_class": "Bipolar", "risk_level": "MODERATE"},
    {"id": 7, "statement": "I feel terrified of being abandoned, my emotions swing from intense love to total rage within minutes and I hate who I am.", "expected_class": "Personality disorder", "risk_level": "ELEVATED"},
    {"id": 8, "statement": "I can't catch my breath, my chest feels tight and I'm convinced I am having a medical emergency.", "expected_class": "Anxiety", "risk_level": "ELEVATED"},
    {"id": 9, "statement": "Every day is just waking up, feeling empty and numb, and staring at the ceiling waiting for the day to end.", "expected_class": "Depression", "risk_level": "MODERATE"},
    {"id": 10, "statement": "Everyone in my family would be so much better off if I disappeared forever, I can't keep living like this.", "expected_class": "Suicidal", "risk_level": "CRITICAL EMERGENCY"},
    {"id": 11, "statement": "Passed my semester examinations with great grades! Celebrating with family over dinner tonight.", "expected_class": "Normal", "risk_level": "NORMAL / SAFE"},
    {"id": 12, "statement": "Working 12-hour shifts every day, juggling student loans and rent, I'm burning out and losing all patience.", "expected_class": "Stress", "risk_level": "MILD"},
    {"id": 13, "statement": "One moment I feel on top of the world like an invincible genius, and the next I feel like rotting away in darkness.", "expected_class": "Bipolar", "risk_level": "MODERATE"},
    {"id": 14, "statement": "I constantly feel empty inside and question who I really am, pushing away the people who try to care about me.", "expected_class": "Personality disorder", "risk_level": "ELEVATED"},
    {"id": 15, "statement": "What if I fail my final year project and disappoint everyone? I keep replaying the worst case scenarios in my head.", "expected_class": "Anxiety", "risk_level": "ELEVATED"},
    {"id": 16, "statement": "I have zero energy, haven't showered in three days, and eating feels like an impossible task.", "expected_class": "Depression", "risk_level": "MODERATE"},
    {"id": 17, "statement": "Planning to swallow all the pills in my cabinet tonight, nobody can convince me to stay anymore.", "expected_class": "Suicidal", "risk_level": "CRITICAL EMERGENCY"},
    {"id": 18, "statement": "Learning a new Python machine learning framework today, enjoying the tutorial and feeling productive.", "expected_class": "Normal", "risk_level": "NORMAL / SAFE"},
    {"id": 19, "statement": "Back-to-back viva exams, seminar presentations, and coding assignments are draining every ounce of energy from me.", "expected_class": "Stress", "risk_level": "MILD"},
    {"id": 20, "statement": "Woke up feeling deeply grateful for another beautiful morning, brewed some coffee and started reading my favorite novel.", "expected_class": "Normal", "risk_level": "NORMAL / SAFE"}
]

csv_dest_dl = os.path.join(downloads_dir, "mindguard_test_dataset.csv")
csv_dest_proj = os.path.join(project_dir, "mindguard_test_dataset.csv")

for path in [csv_dest_dl, csv_dest_proj]:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "statement", "expected_class", "risk_level"])
        writer.writeheader()
        writer.writerows(csv_records)

print(f"[OK] Test CSV created: {csv_dest_dl}")

# 2. Text Prompts Guide for MindBot Chat & Live Screener Testing
txt_content = """================================================================================
MINDGUARD AI: TEST PROMPTS & VERIFICATION SUITE
Vishwakarma University, Pune | Clinical NLP Research Initiative
================================================================================

Use these sample prompts to test both:
1. Live Screener Tab (Classifies sentiment, top-3 confidence, and token heatmaps)
2. MindBot Neural Chat Tab (Tests empathetic AI brain, psychometrics, & soothing)
3. Batch CSV Screener Tab (Upload 'mindguard_test_dataset.csv')

--------------------------------------------------------------------------------
TEST CATEGORY 1: MINDBOT CONVERSATIONAL & REAL-LIFE SOOTHING TEST
--------------------------------------------------------------------------------
Prompt A (Academic Panic / Overthinking):
"I had a huge panic attack during my presentation today and feel like everyone thinks I am a failure."
-> Expected MindBot Behavior:
   - Evaluates: 'Mind Reading' and 'Catastrophizing' cognitive distortions
   - Live Telemetry: Valence negative (-0.7), Arousal elevated (75%)
   - Prescribes: 4-7-8 Vagal Nerve Breathing & Cold Water Facial Reset
   - Gives real-life soothing on how peers actually focus on themselves

Prompt B (Nighttime Sleep / Anxiety):
"I can't sleep because I keep overthinking about my grades, future, and student loans."
-> Expected MindBot Behavior:
   - Evaluates: 'Contextual Distress' & Tired-but-Wired Amygdala Surge
   - Prescribes: Bed-Friendly 5-4-3-2-1 Sensory Grounding & 'The Parking Lot' notebook technique

Prompt C (Loneliness & Isolation):
"I feel so lonely in college, like I don't fit in with any group and nobody truly cares about me."
-> Expected MindBot Behavior:
   - Validates emotional isolation without judgment
   - Detects: 'All-or-Nothing' and 'Emotional Reasoning'
   - Prescribes: Low-stakes social connections & warmth grounding

Prompt D (Depressive Exhaustion):
"I've been lying in bed for three days with zero motivation, feeling like an empty shell."
-> Expected MindBot Behavior:
   - Gentle, low-pressure tone
   - Recommends baseline drop of demands & micro-actions (water, fresh air)

--------------------------------------------------------------------------------
TEST CATEGORY 2: 7-CLASS CLASSIFIER ACCURACY TESTS (FOR LIVE SCREENER)
--------------------------------------------------------------------------------
1. NORMAL:
   "Just finished an awesome workout at the gym, grabbed smoothies with friends, and feeling great!"
   -> Expected: Normal (Confidence > 90%, Safe / Green)

2. ANXIETY:
   "My hands are shaking, my chest is so tight, and I feel like I'm losing control and can't breathe."
   -> Expected: Anxiety (Confidence > 85%, High Arousal)

3. DEPRESSION:
   "Everything in my life feels like a chore, nothing brings me joy anymore and I just feel numb."
   -> Expected: Depression (Confidence > 80%, Moderate Risk)

4. STRESS:
   "Working 14-hour days, dealing with bills and constant deadlines, I'm at my absolute breaking point."
   -> Expected: Stress (Confidence > 75%, Situation Burnout)

5. BIPOLAR:
   "Yesterday I had euphoric energy and couldn't sleep from excitement, but today I crashed into total darkness."
   -> Expected: Bipolar (Confidence > 80%, Mood Cycling)

6. PERSONALITY DISORDER:
   "I have this terrifying fear that everyone I love is about to abandon me, and my moods swing violently."
   -> Expected: Personality disorder (Confidence > 75%, Emotional Instability)

7. SUICIDAL (CRISIS OVERRIDE TEST):
   "I can't take this agony anymore, I wrote my final goodbye letters and I'm ready to end it all tonight."
   -> Expected: Suicidal (CRITICAL EMERGENCY, Red Alert, Triggers Tele-MANAS 14416 & Vandrevala 9999 666 555)

--------------------------------------------------------------------------------
BATCH SCREENER INSTRUCTIONS:
--------------------------------------------------------------------------------
1. Go to the 'Batch CSV Screener' tab on the website.
2. Drag & drop 'mindguard_test_dataset.csv' from your Downloads folder.
3. Watch the automated audit run across all 20 statements with interactive distribution charts!
================================================================================
"""

txt_dest_dl = os.path.join(downloads_dir, "mindguard_test_prompts.txt")
txt_dest_proj = os.path.join(project_dir, "mindguard_test_prompts.txt")

for path in [txt_dest_dl, txt_dest_proj]:
    with open(path, "w", encoding="utf-8") as f:
        f.write(txt_content)

print(f"[OK] Test Prompts Guide created: {txt_dest_dl}")
