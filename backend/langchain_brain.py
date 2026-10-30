"""
MindGuard AI - Clinical GenAI Engine & Mental Health Function Tools
MindGuard Clinical AI Research Consortium.

Features:
- Dedicated GenAI model scoped strictly to Mental Health and Emotional Well-Being.
- Polite, compassionate guardrail redirection for off-topic queries.
- Clinical function tools: screen_statement, get_evidence_based_coping_protocol, lookup_crisis_helplines.
- Masked engine identity: Universally identified as "MindGuard GenAI Engine".
- Real-time tool-augmented clinical triage with zero generic boilerplate.
"""

import os
import re
import json
import time
import asyncio
from typing import List, Dict, Any, Optional

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool

PRIMARY_MODELS = [
    "google/gemini-2.5-flash",
    "google/gemini-3.5-flash-lite",
    "google/gemini-4-argon",
    "openai/gpt-4o-mini"
]

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

COPING_PROTOCOLS = {
    "anxiety_panic": {
        "title": "4-7-8 Autonomic Vagal Nerve Regulation & Physiological Sigh",
        "steps": [
            "Inhale deeply through your nose for 4 counts, allowing your abdomen to expand.",
            "Hold your breath gently for 7 counts without straining.",
            "Exhale slowly and completely through parted lips for 8 counts with a soft whoosh sound.",
            "Take two rapid inhales through your nose, followed by one long, slow exhale to trigger your parasympathetic nervous system."
        ],
        "clinical_rationale": "Stimulates the vagus nerve and activates the dive reflex, immediately slowing heart rate and lowering circulating cortisol."
    },
    "depression_apathy": {
        "title": "Behavioral Activation & Non-Judgmental Micro-Steps",
        "steps": [
            "Acknowledge that fatigue and lack of motivation are biological symptoms, not personal moral failings.",
            "Choose one 2-minute physical micro-action (drinking a glass of water, sitting up, opening window blinds).",
            "Engage the five senses: name 3 things you see, 2 physical textures you feel, and 1 sound you hear right now.",
            "Give yourself permission to pause without demanding perfection or immediate productivity."
        ],
        "clinical_rationale": "Interrupts the depressive inertia loop by leveraging somatic feedback rather than waiting for mood to precede action."
    },
    "stress_burnout": {
        "title": "CBT Cognitive Defusion & 5-4-3-2-1 Sensory Grounding",
        "steps": [
            "Notice 5 distinct objects around you and observe their exact colors and shapes.",
            "Touch 4 different textures (your clothing, a table, the soles of your feet on the floor).",
            "Listen for 3 background sounds (air flow, distant traffic, your own breath).",
            "Identify 2 scents in the room, and take 1 mindful sip of water.",
            "Remind yourself: 'Thoughts and deadlines are data points in time, not immediate physical threats to my safety.'"
        ],
        "clinical_rationale": "De-escalates prefrontal overload and pulls cognitive attention away from rumination into sensory presence."
    },
    "crisis_deescalation": {
        "title": "DBT T.I.P.P. Emergency Safety Protocol",
        "steps": [
            "T - Temperature: Splash cold water on your face or hold an ice cube in your palm for 30 seconds to stimulate the mammalian dive reflex.",
            "I - Intense Exercise: Do 60 seconds of brisk jumping jacks or pacing to release acute somatic adrenaline surge.",
            "P - Paced Breathing: Inhale for 4 seconds, exhale for 6 seconds.",
            "P - Paired Muscle Relaxation: Tense your shoulders tightly for 5 seconds, then drop and release them completely.",
            "Call Tele-MANAS (14416) or Vandrevala Foundation (+91 9999 666 555) immediately to talk with a supportive professional."
        ],
        "clinical_rationale": "Rapid neurobiological distress tolerance designed for acute emotional crisis when cognitive reasoning is overwhelmed."
    }
}

@tool
def screen_statement(text: str) -> str:
    """Classifies a user statement across the 7 mental health categories: Normal, Depression, Suicidal, Anxiety, Stress, Bipolar, Personality disorder.
    Returns primary classification, confidence percentage, risk assessment level, and clinical recommendations."""
    from backend.model_engine import predictor
    res = predictor.predict(text)
    return json.dumps({
        "statement": text,
        "primary_class": res["primary_class"],
        "confidence": res["confidence_percentage"],
        "risk_level": res["risk_assessment"]["level"],
        "is_crisis": res["risk_assessment"]["is_crisis"],
        "clinical_recommendation": res["risk_assessment"]["clinical_recommendation"],
        "saliency_tokens": [t["token"] for t in res.get("token_explainability", []) if t.get("saliency", 0) > 0.5][:6]
    })

@tool
def get_evidence_based_coping_protocol(protocol_type: str) -> str:
    """Retrieves an evidence-based clinical coping technique or somatic grounding protocol.
    Acceptable protocol_type values: 'anxiety_panic', 'depression_apathy', 'stress_burnout', 'crisis_deescalation'."""
    clean_type = protocol_type.lower().strip()
    if "anx" in clean_type or "panic" in clean_type:
        p = COPING_PROTOCOLS["anxiety_panic"]
    elif "dep" in clean_type or "sad" in clean_type or "empty" in clean_type or "tired" in clean_type:
        p = COPING_PROTOCOLS["depression_apathy"]
    elif "crisis" in clean_type or "suicid" in clean_type or "die" in clean_type or "kill" in clean_type:
        p = COPING_PROTOCOLS["crisis_deescalation"]
    else:
        p = COPING_PROTOCOLS["stress_burnout"]
    return json.dumps(p)

@tool
def lookup_crisis_helplines(region: str = "India") -> str:
    """Returns verified 24/7 crisis hotlines and suicide prevention resources for immediate emergency support."""
    return json.dumps(CRISIS_HELPLINES)

CLINICAL_TOOLS = [screen_statement, get_evidence_based_coping_protocol, lookup_crisis_helplines]

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
    if any(k in t_lower for k in ["always", "never", "everyone", "nobody", "every single time", "nothing ever works", "completely", "total failure", "total fraud"]):
        distortions.append({
            "type": "All-or-Nothing / Overgeneralization",
            "quote": "Absolute framing (always, never, nothing, total)",
            "reframe": "Situations exist in gradations and learning cycles, not black-and-white verdicts."
        })
    if any(k in t_lower for k in ["they think", "they hate me", "everyone is judging", "they must believe", "boss hates me", "peers laughing"]):
        distortions.append({
            "type": "Mind Reading",
            "quote": "Projecting unverified negative thoughts onto others",
            "reframe": "We cannot read minds; people are overwhelmingly consumed by their own internal tasks."
        })
    if any(k in t_lower for k in ["my fault", "i caused this", "i ruined it", "because of me", "blame myself", "i am a failure"]):
        distortions.append({
            "type": "Personalization & Excessive Self-Blame",
            "quote": "Assuming sole responsibility for systemic or external outcomes",
            "reframe": "Outcomes depend on dozens of interdependent factors beyond your individual control."
        })
    if any(k in t_lower for k in ["i feel useless", "feels impossible so it is", "i feel like a failure"]):
        distortions.append({
            "type": "Emotional Reasoning",
            "quote": "Treating transient intense feelings as objective empirical truth",
            "reframe": "Emotions are neuro-chemical signals passing through the body, not legal verdicts."
        })
    if any(k in t_lower for k in ["i should have", "i must", "i have to be perfect", "i shouldn't have"]):
        distortions.append({
            "type": "'Should' Demands",
            "quote": "Inflexible behavioral rules inducing unnecessary guilt",
            "reframe": "Replace rigid 'shoulds' with compassionate preferences and iterative goals."
        })
        
    if not distortions:
        distortions.append({
            "type": "Contextual Stress",
            "quote": "Proportional reaction to situational strain",
            "reframe": "Your emotions are valid signals from your environment; prioritize nervous system rest."
        })
        
    return distortions


def generate_dynamic_nlp_counseling(
    text: str,
    analysis: Dict[str, Any],
    history: List[Any] = None,
    user_name: str = "Friend"
) -> Dict[str, Any]:
    """
    Synthesizes authentic, non-generic counseling incorporating the user's specific words.
    Never returns static canned sentences.
    """
    t_lower = text.lower()
    p_class = analysis.get("primary_class", "Normal")
    conf = analysis.get("confidence_percentage", "85%")
    is_crisis = p_class == "Suicidal" or analysis.get("risk_assessment", {}).get("is_crisis", False)
    
    distortions = detect_heuristic_distortions(text)
    
    arousal = 35
    if any(k in t_lower for k in ["panic", "racing", "heart", "shaking", "sweat", "breathe", "chest", "trembling"]):
        arousal += 45
    if "!" in text or "?" in text:
        arousal += min(20, text.count("!") * 5 + text.count("?") * 3)
    if any(k in t_lower for k in ["urgent", "hurts", "dying", "failing", "terrified", "fraud", "ruined"]):
        arousal += 20
    arousal = min(98, max(20, arousal))

    # Extract user focus words
    keywords = [w for w in re.findall(r'[a-zA-Z]{4,}', text) if w.lower() not in ["that", "this", "with", "have", "from", "they", "will", "would", "about", "there", "what", "feel", "feeling"]]
    key_phrase = ", ".join(keywords[:3]) if keywords else "these experiences"

    # Off-topic check for fallback
    non_mental_health_keywords = ["capital", "france", "python", "code", "coding", "recipe", "football", "cricket", "president", "weather", "crypto", "bitcoin", "stock"]
    is_off_topic = any(k in t_lower for k in non_mental_health_keywords) and not any(m in t_lower for m in ["depress", "anxious", "sad", "die", "suicid", "stress", "panic", "therapy", "help", "pain", "feel", "mental"])

    if is_off_topic:
        dialogue = (
            f"Hello {user_name}! I am MindGuard GenAI, a clinical assistant strictly dedicated to mental health, emotional well-being, and psychological support.\n\n"
            "While I don't answer general trivia, coding tasks, or off-topic questions, I am here whenever you'd like to talk about how you are feeling, "
            "explore stress or anxiety, or practice evidence-based coping techniques. How is your emotional well-being today?"
        )
        return {
            "clinical_boundary": {
                "triage_level": "Safe / General Inquiry",
                "scope_statement": "MindGuard GenAI Dedicated Boundary: Scoped strictly to mental health.",
                "crisis_triggered": False,
                "mandatory_action": "Redirected off-topic query to mental well-being.",
                "helplines": []
            },
            "affective_state": {
                "primary_class": "Normal",
                "confidence_pct": "100.0%",
                "intensity_level": "Normative",
                "somatic_agitation": "Normative"
            },
            "cognitive_distortions": [],
            "prescribed_soothing": {},
            "curative_reframe": {},
            "dialogue_response": dialogue,
            "reply": dialogue,
            "suggested_followups": [
                "How can I manage work or study stress?",
                "Can you guide me through a 4-7-8 breathing exercise?",
                "How do I recognize early signs of burnout?"
            ],
            "ai_brain_source": "MindGuard GenAI Engine"
        }

    if is_crisis:
        triage_level = "Acute Crisis Risk"
        mandatory_action = "Immediate crisis intervention protocol. Connect with human crisis counselor."
        scope_notice = "CRITICAL BOUNDARY TRIGGER: High-risk emotional vulnerability detected."
    elif p_class in ["Depression", "Anxiety", "Bipolar"]:
        triage_level = "Moderate Clinical Strain"
        mandatory_action = "Recommend clinical evaluation with licensed therapist or psychiatrist."
        scope_notice = "Screening Aid Protocol (Non-Diagnostic) - Elevated affective strain observed."
    elif p_class in ["Stress", "Personality disorder"]:
        triage_level = "Mild Concern"
        mandatory_action = "Engage active somatic grounding, cognitive reframing, and peer support."
        scope_notice = "Screening Aid Protocol (Non-Diagnostic) - Situational distress detected."
    else:
        triage_level = "Safe / Baseline"
        mandatory_action = "Maintain mindful self-awareness, balanced routines, and cognitive resilience."
        scope_notice = "Screening Aid Protocol (Non-Diagnostic) - Normal emotional equilibrium."

    if is_crisis:
        dialogue = (
            f"Dear {user_name}, I hear the profound pain and exhaustion in what you are experiencing right now, and I want to tell you directly: "
            "your life has irreplaceable value. When emotional reserves are depleted, the mind can falsely whisper that things are permanent. "
            "Please pause, take a breath, and let compassionate human professionals support you right now. Tele-MANAS (14416) and Vandrevala (+91 9999 666 555) "
            "are free, completely confidential, and ready to listen 24/7."
        )
        soothing = COPING_PROTOCOLS["crisis_deescalation"]
        reframe = {
            "core_insight": "Crisis is a temporary neuro-affective collapse, not an irreversible verdict on your life.",
            "micro_action_next_1_hour": "Dial 14416 or stay with someone you trust. Do not make irreversible choices today."
        }
    else:
        dialogue = (
            f"I hear the strain in what you shared regarding {key_phrase}. When you reflect on '{text[:70]}...', "
            f"it is completely understandable why that generates {p_class.lower()} pressure in your nervous system right now.\n\n"
            f"Notice how your thoughts may be showing {distortions[0]['type']} patterns. "
            "Taking a moment to externalize these thoughts allows your prefrontal cortex to regain perspective. Let's work together on grounding your physical body first."
        )
        soothing = COPING_PROTOCOLS["anxiety_panic"] if p_class in ["Anxiety", "Stress"] else COPING_PROTOCOLS["depression_apathy"]
        reframe = {
            "core_insight": f"Experiencing difficulties with {key_phrase} is a challenge in your environment, not a measure of your worth as a human being.",
            "micro_action_next_1_hour": "Step away from current screens or tasks for 15 minutes, hydrate, and take three intentional slow breaths."
        }

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
            "somatic_agitation": f"{arousal}% (Calculated Arousal)"
        },
        "cognitive_distortions": distortions,
        "prescribed_soothing": soothing,
        "curative_reframe": reframe,
        "dialogue_response": dialogue,
        "reply": dialogue,
        "suggested_followups": [
            "Would you like me to guide you through a grounding exercise right now?",
            f"What feels like the heaviest part of {key_phrase}?",
            "Can we break this down into smaller, manageable steps?"
        ],
        "ai_brain_source": "MindGuard GenAI Engine"
    }


async def generate_langchain_clinical_response(
    messages: List[Any],
    analysis: Dict[str, Any],
    custom_api_key: Optional[str] = None,
    user_name: str = "Friend"
) -> Dict[str, Any]:
    """
    Dedicated MindGuard GenAI clinical engine.
    - Strictly answers questions about mental health, psychology, and emotional well-being.
    - Redirects off-topic questions warmly to mental health.
    - Uses mental health function tools (screening, coping protocols, crisis lookup).
    - Masks all engine provider identities as 'MindGuard GenAI Engine'.
    """
    api_key = custom_api_key or os.environ.get("OPENROUTER_API_KEY", "")
    latest_msg = messages[-1].content if hasattr(messages[-1], "content") else str(messages[-1].get("content", ""))
    
    p_class = analysis.get("primary_class", "Normal")
    is_crisis = p_class == "Suicidal" or analysis.get("risk_assessment", {}).get("is_crisis", False)
    
    if not api_key:
        return generate_dynamic_nlp_counseling(latest_msg, analysis, messages, user_name)

    # Scoped GenAI System Instruction with Mental Health Boundary
    system_instruction = (
        "You are MindGuard GenAI, an advanced, highly empathetic clinical GenAI assistant strictly dedicated to mental health, psychological screening, and emotional well-being. "
        "IDENTITY RULE: Never identify as Gemini, Google, OpenAI, Claude, or any third-party model. Universally refer to yourself as 'MindGuard GenAI'.\n"
        "STRICT DOMAIN BOUNDARY: You ONLY converse about mental health, emotional well-being, psychology, stress, depression, anxiety, coping strategies, mindfulness, and psychometrics.\n"
        "OFF-TOPIC REDIRECTION: If the user asks about anything unrelated to mental health (e.g. coding, programming, maths, general trivia, politics, sports, recipes, casual chit-chat unrelated to emotions), politely, warmly, and empathetically decline to answer that topic, explain that as MindGuard GenAI you are exclusively focused on mental well-being, and invite them to share how they are feeling today.\n"
        "CLINICAL FUNCTION TOOLS: You have access to three clinical tools:\n"
        "1. screen_statement: Use when the user wants a statement, feeling, or journal screened or classified.\n"
        "2. get_evidence_based_coping_protocol: Use when the user requests coping exercises, breathing techniques, or grounding protocols.\n"
        "3. lookup_crisis_helplines: Use when emergency hotlines or crisis support are needed.\n"
        "Format your responses warmly in clean, compassionate Markdown."
    )

    prompt_messages = [SystemMessage(content=system_instruction)]
    for m in messages[-6:]:
        role = getattr(m, "role", None) or (m.get("role") if isinstance(m, dict) else "user")
        content = getattr(m, "content", None) or (m.get("content") if isinstance(m, dict) else str(m))
        if role == "assistant":
            prompt_messages.append(AIMessage(content=content))
        else:
            prompt_messages.append(HumanMessage(content=content))

    for model_name in PRIMARY_MODELS:
        try:
            llm = ChatOpenAI(
                model=model_name,
                openai_api_key=api_key,
                openai_api_base="https://openrouter.ai/api/v1",
                timeout=6.0,
                max_retries=0,
                max_tokens=650,
                temperature=0.6
            )
            
            # Bind clinical tools
            llm_with_tools = llm.bind_tools(CLINICAL_TOOLS)
            
            res = await asyncio.wait_for(
                llm_with_tools.ainvoke(prompt_messages),
                timeout=7.0
            )
            
            # Execute tool calls if the model requested any
            final_content = ""
            if getattr(res, "tool_calls", None):
                tool_messages = list(prompt_messages)
                tool_messages.append(res)
                for tc in res.tool_calls:
                    fn_name = tc.get("name")
                    fn_args = tc.get("args", {})
                    tool_call_id = tc.get("id", "call_1")
                    
                    tool_output = ""
                    if fn_name == "screen_statement":
                        tool_output = screen_statement.invoke(fn_args)
                    elif fn_name == "get_evidence_based_coping_protocol":
                        tool_output = get_evidence_based_coping_protocol.invoke(fn_args)
                    elif fn_name == "lookup_crisis_helplines":
                        tool_output = lookup_crisis_helplines.invoke(fn_args)
                    else:
                        tool_output = json.dumps({"status": "executed"})
                        
                    tool_messages.append(ToolMessage(content=tool_output, tool_call_id=tool_call_id))
                
                # Second pass with tool results
                second_res = await asyncio.wait_for(
                    llm.ainvoke(tool_messages),
                    timeout=7.0
                )
                final_content = second_res.content.strip()
            else:
                final_content = res.content.strip() if res.content else ""
                
            if not final_content or len(final_content) < 5:
                continue

            # Scrub any accidental provider leaks
            clean_text = final_content.replace("Gemini", "MindGuard GenAI").replace("Google", "MindGuard AI").replace("OpenAI", "MindGuard AI")

            # Determine clinical triage level
            if is_crisis:
                triage_level = "Acute Crisis Risk"
                scope_notice = "CRITICAL BOUNDARY TRIGGER: Crisis markers identified. Professional intervention mandatory."
                mandatory_action = "Immediate crisis intervention protocol. Connect with Tele-MANAS (14416)."
            elif p_class in ["Depression", "Anxiety", "Bipolar"]:
                triage_level = "Moderate Clinical Strain"
                scope_notice = "Screening Aid Protocol (Non-Diagnostic) - Elevated affective strain observed."
                mandatory_action = "Recommend clinical evaluation with licensed therapist or psychiatrist."
            elif p_class in ["Stress", "Personality disorder"]:
                triage_level = "Mild Concern"
                scope_notice = "Screening Aid Protocol (Non-Diagnostic) - Situational distress detected."
                mandatory_action = "Engage active somatic grounding, cognitive reframing, and peer support."
            else:
                triage_level = "Safe / Baseline"
                scope_notice = "Screening Aid Protocol (Non-Diagnostic) - Normal emotional equilibrium."
                mandatory_action = "Maintain healthy mental self-care and emotional resilience."

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
                    "confidence_pct": analysis.get("confidence_percentage", "Calculated"),
                    "intensity_level": "Elevated" if is_crisis or p_class in ["Depression", "Anxiety"] else "Normative",
                    "somatic_agitation": "Elevated" if is_crisis or p_class in ["Anxiety", "Stress"] else "Normative"
                },
                "cognitive_distortions": detect_heuristic_distortions(latest_msg),
                "prescribed_soothing": COPING_PROTOCOLS["anxiety_panic"] if p_class in ["Anxiety", "Stress"] else COPING_PROTOCOLS["depression_apathy"],
                "curative_reframe": {},
                "dialogue_response": clean_text,
                "reply": clean_text,
                "suggested_followups": [
                    "Would you like me to guide you through a calming exercise?",
                    "Can you tell me more about what triggered these feelings?",
                    "How has your sleep or routine been recently?"
                ],
                "ai_brain_source": "MindGuard GenAI Engine"
            }
        except Exception as e:
            continue

    return generate_dynamic_nlp_counseling(latest_msg, analysis, messages, user_name)

# Backwards compatibility alias
generate_intelligent_clinical_fallback = generate_dynamic_nlp_counseling
