# EmailReplyGenerator
An Email reply generator is made using Langchain and Mistral AI.

# AI Email Reply Generator

A full-stack app that analyzes an incoming email, detects intent, and generates a professional AI reply.

## Features
- Detects intent: Inquiry / Complaint / Offer / Information
- Tones: Formal, Friendly, Persuasive
- Vue frontend + FastAPI backend
- Uses Mistral AI (`mistral-small`)

## Run Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Create `.env` file:
MISTRAL_API_KEY=YOUR_KEY

## Run Frontend
cd frontend
npm install
npm run dev

Node modules will install after frontend is run.

## Deployment
- Backend → FastAPI/Vue
- Frontend → Netlify / Vercel / GitHub Pages

Issues Faced: 
Reply sometimes cannot be generated , but the email can be classified as Inquiry , Complaint or Information. This is because the key issued or the key used is not compatible with mistral-small or there is a response format error. To fix this a full print statement like the one given below can be included.

try:
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    response_json = response.json()

    print("Mistral API response:", response_json)  # <-- debug

    ai_output = response_json.get("completion", "").strip()
    if not ai_output:
        ai_output = "Error: Could not generate reply from Mistral API."

except Exception as e:
    ai_output = "The AI reply could not be generated at this time."
    print("Mistral API error:", str(e))

