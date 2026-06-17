import os
import json
import google.generativeai as genai


API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_message(message):

    prompt = f"""
You are a cybersecurity scam detection expert.

Analyze the message and return ONLY valid JSON.

Identify any psychological manipulation tactics used.

Possible tactics:
- Fear
- Urgency
- Authority
- Greed
- Curiosity
- Scarcity
- Trust Exploitation

risk_score must be an INTEGER between 0 and 100.

Examples:
- Safe message: 0-30
- Suspicious message: 31-70
- Scam or phishing message: 71-100

Do not use decimals.

Return them in the manipulation_tactics array.

Format:

{{
    "risk_score": 0,
    "verdict": "",
    "category": "",
    "manipulation_tactics": [],
    "red_flags": [],
    "explanation": "",
    "recommended_action": ""
}}



Message:
{message}
"""

    response = model.generate_content(prompt)

    print(response.text)
    return json.loads(response.text.replace("```json", "").replace("```", ""))