# SĀRTHI — Sanskrit AI Research & Teaching Helper Interface

A local-first Sanskrit learning chatbot with an ACT (Analyze → Choose → Take Action) pipeline. No external APIs, no cloud databases — everything runs on your machine.

## Features

- Conversational Sanskrit chatbot with intent detection
- Sanskrit ↔ English translation (local dataset)
- Word meaning lookup (50+ words)
- Grammar topics with examples and practice
- Sentence analysis (word-by-word breakdown)
- Sandhi explanation and splitting
- 10 Sanskrit shlokas with meanings and sources
- 8 guided beginner lessons with progress tracking
- 20-question quiz system with scoring
- Voice Studio (speech-to-text and text-to-speech via Web Speech API)
- Chat history with localStorage

## Requirements

- Python 3.11+
- Node.js 18+
- npm
- VS Code (recommended)

## Backend Setup (PowerShell)

```powershell
cd backend

python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

python -m uvicorn app.main:app --reload --port 8000
```

The backend runs at: http://localhost:8000

Health check: http://localhost:8000/api/health

## Frontend Setup (separate PowerShell terminal)

```powershell
cd frontend

npm install

npm run dev
```

The frontend runs at: http://localhost:5173

## Running Tests

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pytest ../tests/ -v
```

## Stopping the Servers

Press `Ctrl + C` in each terminal window.

## Technology Stack

| Layer    | Technology                    |
|----------|-------------------------------|
| Frontend | React, Vite, TypeScript, Tailwind CSS |
| Backend  | Python, FastAPI, Uvicorn      |
| Data     | JSON files (local)            |
| Storage  | Browser localStorage          |

## API Endpoints

| Method | Endpoint               | Description              |
|--------|------------------------|--------------------------|
| GET    | /api/health            | Health check             |
| POST   | /api/chat              | ACT chatbot pipeline     |
| POST   | /api/translate         | Sanskrit ↔ English       |
| POST   | /api/meaning           | Word lookup              |
| POST   | /api/grammar           | Grammar query            |
| GET    | /api/grammar/topics    | All grammar topics       |
| POST   | /api/analyze-sentence  | Sentence breakdown       |
| POST   | /api/sandhi            | Sandhi analysis          |
| GET    | /api/shlokas           | All shlokas              |
| GET    | /api/lessons           | All lessons              |
| GET    | /api/quiz              | Quiz questions           |
| GET    | /api/dictionary        | Full dictionary          |

## Docker (for CI/CD)

```powershell
docker build -t sarthi-sanskrit-bot .
docker run -d -p 8000:8000 sarthi-sanskrit-bot
```

## Project Structure

```
sarthi-sanskrit-bot/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── act/               # ACT pipeline (analyzer, chooser, router)
│   │   ├── services/          # Business logic modules
│   │   └── data/              # JSON datasets
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/        # Sidebar, Markdown, ActStatus
│   │   ├── pages/             # Chat, Learn, Grammar, Shlokas, Quiz, Voice
│   │   ├── services/          # API client
│   │   └── hooks/             # Chat history hook
│   └── package.json
├── tests/                     # pytest test suite
├── Dockerfile
├── Jenkinsfile
└── README.md
```
