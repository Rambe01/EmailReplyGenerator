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

## Deployment
- Backend → Render/Vue
- Frontend → Netlify / Vercel / GitHub Pages
