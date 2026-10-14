# AgriSense

AI-powered crop disease detection and smart farming platform. Designed for hackathon/SIH competitions, this project helps farmers identify crop diseases from leaf images and provides actionable treatment recommendations.

## Features

- Crop disease detection from leaf images using AI
- Treatment recommendations with severity levels
- Crop database with soil, water, and season information
- Weather-based irrigation and disease risk advice
- Real-time analysis with confidence scores
- Responsive web interface

## Quick Start

### Docker (recommended)

```bash
docker-compose up
```

Frontend: http://localhost:3000
Backend API: http://localhost:8000
API docs: http://localhost:8000/docs

### Manual Setup

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Health check |
| POST | /api/predict | Upload image for disease detection |
| GET | /api/crops | List all crops |
| GET | /api/crops/{name} | Get crop details |
| GET | /api/weather-advice | Get farming advice based on weather |

## Tech Stack

- **Backend**: Python 3.12, FastAPI, Pillow, NumPy
- **Frontend**: React 18, TypeScript, Vite
- **Deployment**: Docker Compose

## Project Structure

```
agrisense/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── api/             # REST endpoints
│   │   └── core/            # ML model and knowledge base
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Layout
│   │   ├── pages/           # Dashboard, Detection, Crops, Weather
│   │   └── api/             # API client
│   ├── package.json
│   └── vite.config.ts
└── docker-compose.yml
```

## Hackathon Highlights

- Solves real agricultural problem for Tamil Nadu farmers
- AI/ML integration for image classification
- Complete full-stack solution with clean UI
- Scalable architecture ready for production
- Weather-based intelligence system
