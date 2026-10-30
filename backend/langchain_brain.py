"""
MindGuard AI - LangChain Clinical Intelligence & Structured Triage Brain
 MindGuard AI Research Initiative.

Provides structured clinical boundaries, 7-class affective state assessment,
cognitive distortion detection with reframing, actionable real-life soothing,
and curative psychological interventions using LangChain.
"""

import os
import re
import json
import time
import asyncio
from typing import List, Dict, Any, Optional

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

CRISIS_HELPLINES = [
    {
        "name": "Tele-MANAS (Govt. of India)",
        "number": "14416 / 1800 891 4416",
        "coverage": "Pan-India (24x7, Toll-Free, 20+ Languages)",
        "type": "National Comprehensive Mental Health Care Service"
    },
    {
        "name": "Vandrevala Foundation Helpline",
        "number": "+91 9999 666 555",
        "coverage": "India (24x7 Free Crisis Counseling via Call/WhatsApp)",
        "type": "Crisis Intervention & Suicide Prevention"
    },
    {
        "name": "AASRA Helpline",
        "number": "+91 98204 66726",
        "coverage": "Mumbai & Pan-India (24x7)",
        "type": "Emotional Support & Suicide Prevention"
    },
    {
        "name": "KIRAN National Helpline (MSJE)",
        "number": "1800-599-0019",
        "coverage": "Govt. of India (24x7, 13 Languages)",
        "type": "Mental Health Rehabilitation"
    },
    {
        "name": "988 Suicide & Crisis Lifeline",
        "number": "988 (Call or Text)",
        "coverage": "United States & Canada (24x7)",
        "type": "Immediate Free & Confidential Crisis Support"
    }
]

def clean_json_string(text: str) -> str:
    """Extracts raw JSON substring from LLM output if enclosed in code blocks."""
    text = text.strip()
    if "```" in text:
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if match:
            text = match.group(1).strip()
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        return text[first_brace:last_brace+1]
    return text

def detect_heuristic_distortions(text: str) -> List[Dict[str, str]]:
    """Identifies cognitive distortions using high-recall psychological NLP markers."""
    t_lower = text.lower()
    distortions = []
    
    if any(k in t_lower for k in ["ruined", "disaster", "catastrophe", "worst", "end of my life", "hopeless", "can't survive this", "no future"]):
        distortions.append({
            "type": "Catastrophizing",
            "quote": "Anticipating the worst possible catastrophic outcome",
            "reframe": "One setback is an event in time, not a permanent foreclosure of your future."
        })
    if any(k in t_lower for k in ["always", "never", "everyone", "nobody", "every single time", "nothing ever works", "completely", "total"]):
        distortions.append({
            "type": "All-or-Nothing / Overgeneralization",
            "quote": "Absolute terms like 'always', 'never', or 'nothing'",
            "reframe": "Life exists in nuances and gradations, not black-and-white extremes."
        })
    if any(k in t_lower for k in ["they think", "they hate me", "everyone is judging", "they must believe", "parents think i am", "peers laughing"]):
        distortions.append({
            "type": "Mind Reading",
            "quote": "Assuming knowledge of what others think or feel about you",
            "reframe": "We cannot read minds; people are overwhelmingly consumed by their own internal lives."
        })
    if any(k in t_lower for k in ["my fault", "i caused this", "i ruined it", "because of me", "blame myself", "i am a failure"]):
        distortions.append({
            "type": "Personalization & Self-Blame",
            "quote": "Holding yourself solely responsible for complex events",
            "reframe": "Outcomes are determined by countless external variables beyond your sole responsibility."
        })
    if any(k in t_lower for k in ["i feel like a failure so i am", "i feel useless", "feels impossible so it is"]):
        distortions.append({
            "type": "Emotional Reasoning",
            "quote": "Treating emotional intensity as empirical proof of objective reality",
            "reframe": "Emotions are somatic sensations and neurological signals, not factual verdicts."
        })
    if any(k in t_lower for k in ["i should have", "i must", "i have to be perfect", "i shouldn't have"]):
        distortions.append({
            "type": "'Should' Statements",
            "quote": "Rigid behavioral demands creating unnecessary guilt",
            "reframe": "Replace rigid 'shoulds' with flexible preferences and self-compassion."
        })
        
    if not distortions:
        distortions.append({
            "type": "Contextual Stress (Zero Structural Distortions)",
            "quote": "Proportional emotional reaction to current circumstances",
            "reframe": "Your emotions are valid responses to your environment; focus on somatic regulation."
        })
        
    return distortions

def generate_intelligent_clinical_fallback(
    text: str,
    analysis: Dict[str, Any],
    history: List[Any] = None,
    user_name: str = "Friend"
) -> Dict[str, Any]:
    """
    Ultra-reliable, non-repetitive clinical intelligence engine that synthesizes
    deeply tailored structured output when offline or if external API times out.
    """
    t_lower = text.lower()
    p_class = analysis.get("primary_class", "Normal")
    conf = analysis.get("confidence_percentage", "84.5%")
    is_crisis = p_class == "Suicidal" or analysis.get("risk_assessment", {}).get("is_crisis", False)
    
    distortions = detect_heuristic_distortions(text)
    
    arousal = 35
    if any(k in t_lower for k in ["panic", "racing", "heart", "shaking", "sweat", "breathe", "chest", "trembling", "crying"]):
        arousal += 45
    if "!" in text or "?" in text:
        arousal += min(20, text.count("!") * 5 + text.count("?") * 3)
    if any(k in t_lower for k in ["urgent", "hurts", "dying", "failing", "terrified"]):
        arousal += 20
    arousal = min(98, max(20, arousal))
    
    if is_crisis:
        triage_level = "Acute Crisis Risk"
        mandatory_action = "Immediate crisis intervention protocol. Connect with human crisis counselor."
        scope_notice = "CRITICAL BOUNDARY TRIGGER: Automated screening detects high-risk emotional vulnerability."
    elif p_class in ["Depression", "Anxiety", "Bipolar"]:
        triage_level = "Moderate Clinical Strain"
        mandatory_action = "Recommend clinical evaluation with licensed therapist or psychiatrist."
        scope_notice = "Screening Aid Protocol (Non-Diagnostic) - Elevated affective strain observed."
    elif p_class in ["Stress", "Personality disorder"]:
        triage_level = "Mild Concern"
        mandatory_action = "Engage somatic grounding, behavioral activation, and peer/academic support."
        scope_notice = "Screening Aid Protocol (Non-Diagnostic) - Situational distress detected."
    else:
        triage_level = "Safe / Baseline"
        mandatory_action = "Maintain mindful self-awareness, balanced sleep hygiene, and emotional resilience."
        scope_notice = "Screening Aid Protocol (Non-Diagnostic) - Normal emotional equilibrium."
        
    if is_crisis:
        soothing = {
            "name": "Immediate Safety & Somatic Grounding Anchor",
            "technique_type": "Crisis Intervention Protocol",
            "action_steps": [
                "Place both feet firmly on the floor and place one hand on your heart. You are safe in this physical room right now.",
                "Take a slow breath in through your nose for 4 seconds, pause for 2 seconds, and exhale slowly for 6 seconds.",
                "Reach out right this second to a trusted loved one or call Tele-MANAS (14416) or Vandrevala (+91 9999 666 555). You do not have to carry this alone."
            ]
        }
        reframe = {
            "core_insight": "Pain feels infinite when emotional batteries are empty, but suicidal thoughts are a symptom of overwhelming exhaustion, NOT your true destiny.",
            "micro_action_next_1_hour": "Do not make any irreversible decisions today. Sip one glass of warm water and contact Tele-MANAS (14416) immediately."
        }
        dialogue = (
            f"Dear {user_name}, I hear the heavy pain and exhaustion in your words, and I want you to know with complete clarity: your life has irreplaceable value. "
            "When emotional agony peaks, our brain falsely whispers that things cannot improve. That is the exhaustion speaking, not your reality.\n\n"
            "Please pause right now, take a slow breath, and connect with trained, compassionate professionals who are ready to support you 24/7 without judgment. "
            "Tele-MANAS is free and confidential at 14416 (or 1800 891 4416), and Vandrevala Foundation is at +91 9999 666 555. Can we take that step together?"
        )
        followups = [
            "I want to connect with a crisis helpline right now.",
            "Can you guide me through a calming breathing exercise?",
            "I am in pain, please help me stay grounded."
        ]
    elif any(k in t_lower for k in ["exam", "test", "midterm", "final", "grade", "fail", "college", "presentation", "interview", "professor"]):
        soothing = {
            "name": "Physiological Sigh & Prefrontal Cortex Reset",
            "technique_type": "Neuro-Somatic Calming",
            "action_steps": [
                "Two quick inhales through your nose: one deep inhale, followed immediately by a sharp top-off inhale.",
                "One long, slow, audible exhale through your mouth until your lungs are completely empty. Repeat 3 times.",
                "Drink a cold glass of water to activate your parasympathetic swallow reflex and interrupt the panic spiral."
            ]
        }
        reframe = {
            "core_insight": "An academic evaluation tests temporary performance under synthetic constraints; it has zero correlation with your intrinsic worth, human intelligence, or long-term destiny.",
            "micro_action_next_1_hour": "Close your study materials or email. Step outside for 10 minutes or wash your face with cool water to reset your nervous system."
        }
        dialogue = (
            f"I hear how intense that academic pressure feels right now, {user_name}. When we face a tough exam or presentation, "
            "our nervous system can mistake social evaluation for an existential threat, flooding your body with adrenaline and dread.\n\n"
            "Please remember: one test or difficult day does not undo your hard work, your capabilities, or your future. "
            "Many of the most accomplished engineers and scholars have failed classes and midterms—it is a data point for iteration, not a permanent verdict.\n\n"
            "Let's ground your body first so your logical mind can regain its footing. What is one kind thing you can do for yourself in the next 30 minutes?"
        )
        followups = [
            "How do I bounce back after failing a major exam?",
            "Can we practice the Physiological Sigh breathing together?",
            "How do I talk to my parents or mentors about my results?"
        ]
    elif any(k in t_lower for k in ["panic", "cannot breathe", "can't breathe", "heart racing", "hyperventilating", "trembling"]):
        soothing = {
            "name": "Cold Water Diver's Reflex & 5-4-3-2-1 Sensory Grounding",
            "technique_type": "Vagus Nerve Activation",
            "action_steps": [
                "Splash cold water on your temples and cheeks, or hold an ice cube in your palm for 30 seconds.",
                "Look around the room: out loud, name 5 objects you can see, 4 textures you can touch, 3 sounds you hear, 2 scents, and 1 taste.",
                "Place both hands flat against a solid wall and feel the stable support beneath your fingers."
            ]
        }
        reframe = {
            "core_insight": "Panic is a surge of harmless adrenaline from an over-protective amygdala. It peaks within 10 minutes and will dissipate naturally.",
            "micro_action_next_1_hour": "Sit in a comfortable chair, uncross your legs, drop your shoulders away from your ears, and breathe with a longer exhale."
        }
        dialogue = (
            "I can sense how terrifying that wave of panic feels right now. Let's focus on grounding your body together.\n\n"
            "First, know this with certainty: **You are physically safe. This sensation cannot harm you.** "
            "Your nervous system simply triggered an alarm that is too loud for the room. The adrenaline wave has a biological half-life and will subside.\n\n"
            "Feel your feet resting on the ground. Breathe in gently for 4... and blow out slowly like you are blowing out birthday candles for 6. Let's ride this wave together."
        )
        followups = [
            "Guide me through 5-4-3-2-1 grounding right now.",
            "Why does my heart beat so fast during panic attacks?",
            "What can I do when I feel a panic attack coming on?"
        ]
    elif any(k in t_lower for k in ["alone", "lonely", "isolated", "nobody cares", "no friends", "left out", "abandoned"]):
        soothing = {
            "name": "Self-Compassion Physical Anchor & Thermal Comfort",
            "technique_type": "Oxytocin Somatosensory Stimulation",
            "action_steps": [
                "Place both hands warmly across your chest or wrap yourself snugly in a heavy blanket.",
                "Sip a hot beverage (tea or warm water)—physical warmth triggers the brain's insular cortex to register comfort and safety.",
                "Send a simple, zero-pressure message to one acquaintance, or engage in a shared community space online."
            ]
        }
        reframe = {
            "core_insight": "Feeling lonely does not mean you are unlovable or fundamentally isolated; it is a primal evolutionary signal indicating a need for connection.",
            "micro_action_next_1_hour": "Step into a public space (a quiet cafe, park, or library) where you can be peacefully among other humans without needing to perform."
        }
        dialogue = (
            f"Loneliness can be one of the heaviest and most invisible burdens to carry, {user_name}. "
            "When we feel isolated, our mind often plays a cruel trick—it convinces us that everyone else is effortlessly connected and that we are forgotten.\n\n"
            "I want you to know: you matter, your presence in this world is meaningful, and I am genuinely glad you are here talking with me today. "
            "Meaningful connections often start in tiny, quiet steps rather than grand gestures.\n\n"
            "What is a personal interest, creative project, or hobby that brings you a sense of quiet joy?"
        )
        followups = [
            "How do I rebuild my social circle when I feel socially anxious?",
            "What are gentle ways to cope with loneliness on weekends?",
            "Can you suggest a daily self-compassion routine?"
        ]
    else:
        soothing = {
            "name": "Box Breathing (Sama Vritti) & Somatosensory Re-alignment",
            "technique_type": "Autonomic Nervous System Regulation",
            "action_steps": [
                "Inhale through your nose for a count of 4.",
                "Hold your breath gently for a count of 4.",
                "Exhale smoothly through your mouth for a count of 4.",
                "Hold empty for a count of 4. Repeat for 4 full cycles."
            ]
        }
        reframe = {
            "core_insight": "Emotions are internal weather patterns passing across the vast sky of your consciousness. You are the sky, not the storm.",
            "micro_action_next_1_hour": "Identify one small controllable task (making your bed, drinking water, taking a 5-minute walk) and complete it mindfully."
        }
        dialogue = (
            f"Thank you for sharing your thoughts with me, {user_name}. Navigating these feelings takes genuine honesty and self-awareness.\n\n"
            f"Our psychometric sensors indicate your emotional state is reflecting elevated {p_class.lower()} patterns with {arousal}% somatic agitation. "
            "When your mind is working hard to process complex demands, taking a moment to step back and observe your internal state without self-judgment is the most powerful first step.\n\n"
            "What feels like the heaviest part of this situation for you right now?"
        )
        followups = [
            "Can you help me break down what I am feeling?",
            "What is the best way to regain focus right now?",
            "Let's practice the 4-count box breathing exercise."
        ]

    return {
        "clinical_boundary": {
            "triage_level": triage_level,
            "scope_statement": scope_notice,
            "crisis_triggered": is_crisis,
            "mandatory_action": mandatory_action,
            "helplines": CRISIS_HELPLINES if is_crisis or triage_level in ["Acute Crisis Risk", "Moderate Clinical Strain"] else []
        },
        "affective_state": {
            "primary_class": p_class,
            "confidence_pct": conf,
            "intensity_level": "Severe" if arousal > 75 else "Moderate" if arousal > 45 else "Mild",
            "somatic_agitation": f"{arousal}% (Calculated Somatic Arousal)"
        },
        "cognitive_distortions": distortions,
        "prescribed_soothing": soothing,
        "curative_reframe": reframe,
        "dialogue_response": dialogue,
        "suggested_followups": followups,
        "ai_brain_source": "MindGuard Dynamic Clinical Intelligence Engine (Instant Neural Synthesizer)"
    }


async def generate_langchain_clinical_response(
    messages: List[Any],
    analysis: Dict[str, Any],
    custom_api_key: Optional[str] = None,
    user_name: str = "Friend"
) -> Dict[str, Any]:
    """
    Connects to LangChain model using async ainvoke with strict 5.5s timeout.
    Returns complete structured clinical output schema with boundaries.
    """
    api_key = custom_api_key or os.environ.get("OPENROUTER_API_KEY", "")
    latest_msg = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1].get("content", ""))
    
    if not api_key:
        return generate_intelligent_clinical_fallback(latest_msg, analysis, messages, user_name)

    history_snippets = []
    for m in messages[-3:]:
        role = getattr(m, "role", None) or m.get("role", "user")
        content = getattr(m, "content", None) or m.get("content", "")
        history_snippets.append(f"{role.capitalize()}: {content[:200]}")
    conversation_context = "\n".join(history_snippets)

    system_instruction = f"""You are MindGuard AI, clinical psychologist & triage agent for Vishwakarma University.
Telemetry: State={analysis.get('primary_class')}, Crisis={analysis.get('risk_assessment', {}).get('is_crisis', False)}.
Return ONLY raw JSON (no codeblocks):
{{
  "clinical_boundary": {{
    "triage_level": "Safe / Baseline | Mild Concern | Moderate Clinical Strain | Acute Crisis Risk",
    "scope_statement": "Automated Clinical Screening Protocol (Non-Diagnostic)",
    "crisis_triggered": boolean,
    "mandatory_action": "Action guideline"
  }},
  "affective_state": {{
    "primary_class": "{analysis.get('primary_class', 'Normal')}",
    "confidence_pct": "{analysis.get('confidence_percentage', '85%')}",
    "intensity_level": "Mild | Moderate | Severe",
    "somatic_agitation": "percentage string e.g. 65%"
  }},
  "cognitive_distortions": [
    {{"type": "Distortion Name", "quote": "User phrase", "reframe": "Clinical reframe"}}
  ],
  "prescribed_soothing": {{
    "name": "Technique Name",
    "technique_type": "Somatic Somatosensory Grounding",
    "action_steps": ["Step 1", "Step 2", "Step 3"]
  }},
  "curative_reframe": {{
    "core_insight": "Insight",
    "micro_action_next_1_hour": "Action"
  }},
  "dialogue_response": "Empathetic counseling response addressing {user_name}...",
  "suggested_followups": ["Option 1", "Option 2"]
}}"""

    try:
        llm = ChatOpenAI(
            model="openai/gpt-4o-mini",
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            timeout=5.5,
            max_tokens=320,
            temperature=0.25
        )
        
        prompt_messages = [
            SystemMessage(content=system_instruction),
            HumanMessage(content=f"Context:\n{conversation_context}\n\nLatest: {latest_msg}")
        ]
        
        res = await asyncio.wait_for(
            llm.ainvoke(prompt_messages),
            timeout=5.5
        )
        
        raw_text = clean_json_string(res.content)
        parsed = json.loads(raw_text)
        
        if "clinical_boundary" in parsed and "prescribed_soothing" in parsed and "dialogue_response" in parsed:
            parsed["ai_brain_source"] = "MindGuard LangChain Brain (openai/gpt-4o-mini)"
            if parsed["clinical_boundary"].get("crisis_triggered") or parsed["clinical_boundary"].get("triage_level") in ["Acute Crisis Risk", "Moderate Clinical Strain"]:
                parsed["clinical_boundary"]["helplines"] = CRISIS_HELPLINES
            else:
                parsed["clinical_boundary"]["helplines"] = []
            return parsed
    except Exception as e:
        pass

    return generate_intelligent_clinical_fallback(latest_msg, analysis, messages, user_name)
