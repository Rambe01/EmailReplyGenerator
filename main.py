from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "mistral-small"
API_URL = "https://api.mistral.ai/v1/chat/completions"

# Debug: make sure API key is loaded
print("Loaded Mistral API key:", MISTRAL_API_KEY)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class EmailRequest(BaseModel):
    email_text: str
    tone: str

# Simple keyword-based intent detection
def detect_intent(email):
    email_lower = email.lower()
    if "price" in email_lower or "details" in email_lower or "information" in email_lower:
        return "Inquiry"
    if "not happy" in email_lower or "issue" in email_lower or "complaint" in email_lower:
        return "Complaint"
    if "offer" in email_lower or "proposal" in email_lower or "collaboration" in email_lower:
        return "Offer"
    return "Information"

# Build prompt for Mistral
def build_prompt(email, tone):
    return f"""
Classify the intent of this email and write a professional reply in a {tone} tone.

Email:
{email}

Your response should ONLY include the professional reply text.
"""

@app.post("/analyze")
def analyze_email(request: EmailRequest):
    intent = detect_intent(request.email_text)
    prompt = build_prompt(request.email_text, request.tone)

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": MISTRAL_API_KEY  # <-- fixed key header
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise error if status != 200
        response_json = response.json()

        # Mistral-small returns generated text in 'completion'
        ai_output = response_json.get("completion", "").strip()

        if not ai_output:
            ai_output = "Error: Could not generate reply from Mistral API."

    except Exception as e:
        # Fallback reply if API fails
        ai_output = (
            "The AI reply could not be generated at this time. "
            "You can edit this draft manually."
        )
        print("Mistral API error:", str(e))

    return {
        "intent": intent,
        "reply": ai_output,
        "tone_used": request.tone
    }
