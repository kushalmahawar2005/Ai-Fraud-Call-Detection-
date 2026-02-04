import re

# Scam keywords with associated risk weights (0-100 scale impact)
# Higher weight = stronger indicator of a scam
SCAM_KEYWORDS = {
    "otp": 30,
    "pin": 30,
    "cvv": 30,
    "password": 30,
    "bank account": 25,
    "credit card": 25,
    "debit card": 25,
    "expire": 20,
    "block": 20,
    "verification": 15,
    "verify": 15,
    "kyc": 25,
    "update": 10,
    "refund": 20,
    "lottery": 25,
    "prize": 25,
    "winner": 20,
    "urgent": 15,
    "immediately": 15,
    "action required": 15,
    "police": 20,
    "customs": 20,
    "rbi": 15,
    "tax": 15,
    "click": 10,
    "link": 10,
    "apk": 25,
    "download": 10,
    "anydesk": 40,
    "teamviewer": 40,
    "remote support": 30
}

# Heuristics for human voice indicators
HUMAN_FILLERS = [
    "um", "uh", "hmm", "ah", "err", "like", "you know", "i mean", "actually", "basically"
]

def analyze_text(text):
    """
    Analyzes the text for scam indicators.
    Returns a dictionary with risk score, verdict, and matched keywords.
    """
    if not text:
        return {
            "risk_score": 0,
            "verdict": "SAFE",
            "matched_keywords": []
        }

    text_lower = text.lower()
    matched_keywords = []
    total_score = 0
    
    # Check for keywords
    for keyword, weight in SCAM_KEYWORDS.items():
        # Simple substring check (effective for hackathon level)
        if keyword in text_lower:
            matched_keywords.append(keyword)
            total_score += weight
    
    # Calculate Risk Score (Cap at 100)
    risk_score = min(total_score, 100)
    
    # Determine Verdict
    if risk_score <= 30:
        verdict = "SAFE"
    elif risk_score <= 60:
        verdict = "SUSPICIOUS"
    else:
        verdict = "SCAM"
        
    return {
        "risk_score": risk_score,
        "verdict": verdict,
        "matched_keywords": matched_keywords
    }

def detect_voice_authenticity(text):
    """
    Analyzes text structure to estimate if it's AI/Recorded or Human.
    Returns: ai_score (0-100), label, reason
    """
    if not text:
        return 50, "Uncertain", "No audio content."

    text_lower = text.lower()
    ai_score = 50  # Start at neutral
    reasons = []

    # 1. Check for Human Fillers (Decrease AI Score)
    filler_count = 0
    for filler in HUMAN_FILLERS:
        # Check for standalone filler words (e.g. " um ", " uh ")
        # Using regex to ensure we don't match substrings like "thUMb"
        if re.search(rf"\b{filler}\b", text_lower):
            filler_count += 1
    
    if filler_count > 0:
        ai_score -= (filler_count * 15)
        reasons.append(f"Detected natural fillers ({filler_count})")
    else:
        ai_score += 10
        reasons.append("No natural pause words detected")

    # 2. Check Sentence Structure (Narrative/Formal = Higher AI)
    sentences = [s for s in re.split(r'[.!?]', text) if s.strip()]
    if not sentences:
        avg_len = 0
    else:
        avg_len = sum(len(s.split()) for s in sentences) / len(sentences)

    if avg_len > 20:
        ai_score += 20
        reasons.append("Long, structured sentences detected")
    elif avg_len < 8:
        ai_score -= 10
        reasons.append("Short, conversational phrasing")

    # 3. Clamp Score
    ai_score = max(0, min(100, ai_score))

    # 4. Label
    if ai_score < 40:
        label = "Likely Human"
    elif ai_score > 60:
        label = "Likely AI / Pre-recorded"
    else:
        label = "Uncertain / Scripted Human"

    explanation = "; ".join(reasons)
    
    return {
        "score": ai_score,
        "label": label,
        "explanation": explanation
    }
