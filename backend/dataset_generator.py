"""
Dataset generator and corpus manager for Mental Health Sentimental Analysis.
Reflects the Sentiment Analysis for Mental Health dataset (~52,680 records) 
across 7 classes as documented in MindGuard AI Research Initiative Research Paper:
Normal, Depression, Suicidal, Anxiety, Stress, Bipolar, Personality disorder.
"""

import os
import random
import pandas as pd
import json

CLASSES = [
    "Normal",
    "Depression",
    "Suicidal",
    "Anxiety",
    "Stress",
    "Bipolar",
    "Personality disorder"
]

CLASS_DISTRIBUTION = {
    "Normal": 0.310,
    "Depression": 0.292,
    "Suicidal": 0.202,
    "Anxiety": 0.073,
    "Bipolar": 0.053,
    "Stress": 0.049,
    "Personality disorder": 0.021
}

# Authentic linguistic pattern templates per class reflecting real clinical/online statements
VOCABULARY_CORPUS = {
    "Normal": [
        "Today was a great day and I'm feeling really good about life and work.",
        "Just finished my evening jog in the park, feeling refreshed and ready for tomorrow.",
        "Had coffee with an old friend from college and we caught up on so many memories.",
        "Cooked a nice homemade pasta dinner with family and watched a comedy movie.",
        "Excited for the upcoming weekend trip with colleagues, planning the itinerary now.",
        "Completed reading a fascinating book on astronomy, really inspiring ideas.",
        "Productive workday today, solved two tough bugs and got positive feedback from team lead.",
        "Looking forward to the music concert this Sunday, got tickets finally!",
        "Woke up early, watched the sunrise, and enjoyed a quiet morning meditation.",
        "Feeling peaceful and content with where things are heading right now.",
        "Visited the local farmers market and bought fresh fruits and vegetables.",
        "Enjoyed working on my DIY garden project today, flowers are starting to bloom.",
        "Had a relaxing Sunday afternoon doing laundry and listening to my favorite playlist.",
        "Passed my semester exams with good grades, celebrating with my roommates tonight.",
        "Started learning acoustic guitar today, fingers hurt but feeling optimistic.",
        "Nice quiet walk after dinner around the neighborhood, night breeze is so calming.",
        "Finished painting my room a fresh shade of blue, looks so bright and cozy.",
        "Feeling grateful for supportive friends and a warm cup of hot chocolate.",
        "Going to sleep early tonight feeling satisfied with today's achievements.",
        "Just adopted a stray puppy from the shelter, bringing so much joyful energy home!"
    ],
    "Depression": [
        "I feel like an empty hollow shell going through the motions every single day.",
        "Nothing brings me joy anymore, even things I used to love feel meaningless and dull.",
        "Struggling to get out of bed in the morning, everything feels like an impossible chore.",
        "I have this heavy dark cloud over me that never seems to clear away.",
        "Haven't showered or eaten properly in three days, I just feel numb and paralyzed.",
        "I feel completely isolated and lonely even when surrounded by smiling people.",
        "There is this lingering sense of deep sorrow and despair that I cannot shake off.",
        "I feel exhausted down to my bones, sleep does not refresh me anymore.",
        "Nobody really understands the quiet agony of feeling utterly detached from reality.",
        "Lost all motivation for my degree and future career, I feel like a complete failure.",
        "I sit in a dark room staring at the wall for hours wondering why I exist.",
        "Crying uncontrollably in the bathroom again for no apparent reason.",
        "The sadness feels physical, like a suffocating weight pressing down on my chest.",
        "Every single goal I had feels pointless now, what is even the point of trying?",
        "I push everyone away because I don't want to be a toxic burden to their lives.",
        "Guilt and worthlessness keep replaying in my mind over and over again.",
        "It's like looking through glass at the world outside where everyone else is happy.",
        "No matter how much I sleep, I wake up tired of living this repetitive emptiness.",
        "I can't remember the last time I felt genuine spontaneous laughter or happiness.",
        "I feel invisible to everyone around me, slowly fading into the background."
    ],
    "Suicidal": [
        "I cannot take this unbearable agony anymore, I just want all of this pain to permanently stop.",
        "Writing this as a goodbye, I feel my family would be so much better off without me.",
        "Thinking about ending it all tonight, I have already gathered the pills and written the note.",
        "Every breath feels like torture, I don't see any reason to wake up tomorrow morning.",
        "I am looking at the balcony ledge and wondering if jumping will finally bring eternal silence.",
        "Nobody would notice or care if I disappeared from this earth forever.",
        "I have made peace with the decision to die, giving away my possessions to friends.",
        "The thought of suicide is the only comforting relief that crosses my mind these days.",
        "I don't want to fight this darkness anymore, I am ready to let go and end my life.",
        "Please forgive me for what I am about to do tonight, I cannot survive this torment.",
        "I have researched the most painless way to hang myself and I am ready to follow through.",
        "I am a hopeless burden to everyone and suicide is the only rational exit left.",
        "Holding the bottle of sleeping pills in my shaking hands, this nightmare will end soon.",
        "I don't want another day in this body and mind, I want complete non-existence.",
        "Saying my final goodbyes silently in my head to everyone I loved.",
        "There is no future, no hope, no salvation, just a deep void calling me to jump.",
        "I feel dead inside already, making it physical is just finishing the pending paperwork.",
        "I don't want help, I just want the courage to finally pull the trigger and end it.",
        "All the exits are closed except one, and tonight I am finally taking that final exit.",
        "Goodbye world, I am sorry I wasn't strong enough to stay and endure this suffering."
    ],
    "Anxiety": [
        "My heart is pounding uncontrollably in my chest and I feel like I cannot catch my breath.",
        "I am terrified that something horrible and catastrophic is about to happen any second.",
        "Having a sudden panic attack in the crowded subway, hands are shaking and dizzy.",
        "I can't stop overthinking every single tiny social interaction I had today.",
        "Constant tight knot in my stomach and nausea before giving any presentation.",
        "Paralyzed by fear of failing and disappointing everyone who relies on me.",
        "What if I lose control of my mind and faint in front of everybody?",
        "Woke up at 3 AM gasping for air with a racing pulse and sweating palms.",
        "Overwhelmed by intrusive racing thoughts that I cannot silence or pause.",
        "Feeling hypervigilant, scanning the room constantly waiting for danger to strike.",
        "My throat feels tight, like I am choking, even though doctor says my lungs are fine.",
        "Paranoid that everyone is silently judging me, scrutinizing every word I speak.",
        "Can't send a simple email without re-reading it 25 times terrified of a mistake.",
        "Agoraphobia is worsening, the thought of leaving my apartment makes me panic.",
        "Sensory overload in grocery stores makes me want to drop my basket and run away.",
        "Trembling hands, dizziness, and feeling like the ground beneath me is swaying.",
        "Fear of health emergencies, checking my heart rate monitor every two minutes.",
        "Feeling on edge constantly, any sudden loud noise sends adrenaline spiking.",
        "Anticipatory dread ruining every celebration or holiday before it even begins.",
        "Exhausted from living in a permanent fight-or-flight panic cycle every day."
    ],
    "Stress": [
        "Completely drowning under overlapping academic deadlines and back-to-back exams.",
        "Working 14 hours a day with zero rest, my brain feels fried and overwhelmed.",
        "Struggling to juggle two jobs, college tuition payments, and mounting utility bills.",
        "Burnout has set in hard, too many responsibilities on my shoulders without any help.",
        "My manager keeps piling impossible expectations on me while cutting project deadlines.",
        "Tension headaches every afternoon from staring at spreadsheets and endless emails.",
        "Feeling irritable and snapping at my loved ones because of immense pressure at office.",
        "Constantly rushing against the clock, haven't taken a single day off in four months.",
        "Cannot relax even on weekends, my mind keeps obsessing over unfinished to-do lists.",
        "Too many urgent demands pulling me in opposite directions, feeling pulled apart.",
        "Sleepless nights worrying about quarterly performance reviews and impending layoffs.",
        "Back pain and neck stiffness from hunching over laptop working till 2 AM every night.",
        "Financial crunch is suffocating, unexpected hospital bills drained all emergency savings.",
        "No work-life balance left, feeling like an overworked cog in an endless corporate machine.",
        "Feeling chronically stretched thin trying to be a perfect parent, employee, and student.",
        "So much pending work that I don't even know where to start, mental gridlock.",
        "Physical exhaustion catching up, catching colds repeatedly from chronic high stress.",
        "Skipping meals because there isn't even 15 minutes between consecutive client calls.",
        "The cognitive load is too heavy, I am forgetting simple things like keys and passwords.",
        "High cortisol levels making my blood pressure spike, need a genuine break from life."
    ],
    "Bipolar": [
        "Last week I was on top of the world working 72 hours without sleep, today I cannot get up.",
        "Extreme swings between uncontrollable manic euphoria and devastating black depression.",
        "During my manic episode I spent my entire month's salary on impulsive online shopping.",
        "My thoughts were racing so fast that words couldn't keep up with the electricity in my brain.",
        "Felt like a god who unlocked the secrets of the universe, now crashing back into dust.",
        "The sudden transition from laughing wildly to sobbing in despair within hours is exhausting.",
        "Engaged in reckless risky behaviors during the manic high that I deeply regret now.",
        "My family walks on eggshells around me because my mood changes like unpredictable lightning.",
        "Hypomania makes me feel invincible and brilliant, but the inevitable depressive crash is brutal.",
        "I start ten giant creative projects with intense grandiosity and abandon all of them during the slump.",
        "Brain buzzing with hyper-creative energy at 4 AM, believing I don't need human sleep.",
        "Rapid cycling mood states leaving me emotionally disoriented and exhausted.",
        "In the depressive phase, all the grand promises I made during mania become heavy burdens.",
        "I feel like two entirely distinct humans trapped in one alternating biological body.",
        "Irritability and agitation when anyone tries to slow down my racing manic momentum.",
        "Struggling to maintain steady relationships because one week I love, next week I detach.",
        "The euphoric rush feels intoxicating, but the comedown is a terrifying bottomless pit.",
        "Medication helps stabilize the peaks, but I sometimes miss the vivid manic highs.",
        "Unpredictable shifts in energy levels making it almost impossible to hold a routine 9-to-5.",
        "Living with bipolar disorder feels like riding an intense rollercoaster with broken brakes."
    ],
    "Personality disorder": [
        "Terrified of abandonment, one moment I idolize my partner and the next I despise them.",
        "Chronic unstable sense of self, I don't even know who I truly am beneath the masks.",
        "Intense fear of rejection makes me lash out aggressively at the people who care about me.",
        "Splitting behavior: people are either absolute angels or evil monsters in my eyes, no in-between.",
        "Impulsive self-harming tendencies whenever I feel emotionally invalidated or dismissed.",
        "Deep chronic feelings of emptiness that I try to fill with volatile relationships and chaos.",
        "Paranoid ideation under interpersonal stress, convinced people are manipulating me.",
        "Explosive inappropriate anger followed immediately by profound shame and remorse.",
        "Drastic shifts in career goals, sexual identity, values, and friendship groups.",
        "Struggling with borderline personality traits, feeling emotional burns at third-degree intensity.",
        "My emotional reactions are like an exposed nerve ending reacting violently to slight touch.",
        "Intense distrust of therapists and friends, constantly testing if they will abandon me.",
        "Dissociative episodes where I feel completely disconnected from my physical body.",
        "Difficulty recognizing that other people have separate minds, boundaries, and lives.",
        "Unstable emotional dysregulation ruining another close partnership I desperately wanted.",
        "Feeling misunderstood by society, labeled as 'dramatic' when the psychological pain is excruciating.",
        "Engaging in self-sabotage just when things are going stably because chaos feels familiar.",
        "Extreme sensitivity to perceived slight or non-verbal rejection in casual conversation.",
        "Identity diffusion: adopting the personality and accent of whoever I am currently around.",
        "Living with borderline personality disorder is fighting a daily war for emotional equilibrium."
    ]
}

def generate_benchmark_dataset(target_count=2000, output_csv="data/mental_health_benchmark_corpus.csv"):
    """
    Generates a stratified representative dataset matching the Kaggle corpus distribution
    as documented in Table I of the research paper.
    """
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    records = []
    
    for cls_name, share in CLASS_DISTRIBUTION.items():
        cls_count = int(round(target_count * share))
        templates = VOCABULARY_CORPUS[cls_name]
        for _ in range(cls_count):
            # Pick a template or create slight variation
            statement = random.choice(templates)
            # Add slight variations to simulate raw text
            variations = [
                statement,
                statement.lower(),
                statement + " " + random.choice(["Really need support.", "Can anyone relate?", "Feeling this today.", "Just needed to vent.", ""]),
                statement.replace(".", "..."),
            ]
            chosen = random.choice(variations).strip()
            records.append({"statement": chosen, "status": cls_name})
            
    df = pd.DataFrame(records)
    # Shuffle
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv(output_csv, index=False)
    print(f"Generated {len(df)} stratified statements saved to: {output_csv}")
    
    # Save a clean JSON of sample statements for quick UI demonstration
    samples_dict = {}
    for cls_name, items in VOCABULARY_CORPUS.items():
        samples_dict[cls_name] = items[:4]
    
    samples_path = os.path.join(os.path.dirname(output_csv), "test_samples.json")
    with open(samples_path, "w", encoding="utf-8") as f:
        json.dump(samples_dict, f, indent=2)
    print(f"Saved sample demonstration dictionary to: {samples_path}")
    return df

if __name__ == "__main__":
    generate_benchmark_dataset()
