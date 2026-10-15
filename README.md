# AgriSense

AI-powered crop disease detection and smart farming platform for Tamil Nadu farmers. SIH / hackathon ready, production grade.

## Problem Statement

Indian farmers lose 30-40 percent of crop yield annually to late disease detection and lack of access to agricultural experts, especially in rural Tamil Nadu where extension services are limited. A farmer notices leaf spots, has no expert nearby, sprays the wrong pesticide, loses the crop and the money.

## Unique Solution

AgriSense is an offline-first, lightweight expert in the browser:

- Real computer vision with no GPU needed: HSV analysis, leaf segmentation, Sobel edges, GLCM texture, lesion ratios, calibrated softmax scoring across 10 diseases
- Tamil Nadu first knowledge base: 20+ crops, disease lifecycles, pesticide database with dosage, organic alternatives for every disease
- Decision support, not just detection: crop rotation planner, fertilizer calculator by soil and acreage, seasonal calendar, yield prediction, market prices
- Weather disease-risk engine: irrigation advice from temperature, humidity, rain probability and soil type, plus fungal-risk warnings
- Farmer UX: drag-drop batch upload, confidence gauge, treatment cards, disease encyclopedia, EN/TA toggle, downloadable text report, weather dashboard
- Guardrails: 10MB limit, rate limiting, model-status endpoint, full pytest suite

## Features

- 10-class disease detection with calibrated confidence
- Leaf segmentation + HSV + Sobel + GLCM pipeline
- Batch prediction (max 10 images)
- Disease encyclopedia with search and filters
- 20+ crop database for Tamil Nadu
- Rotation planner, fertilizer calculator, farming calendar
- Yield prediction, market prices, pest lifecycles
- Weather irrigation + disease-risk APIs
- EN/TA language toggle, mobile responsive
- Docker Compose one-command demo

## Quick Start

### Docker

```bash
docker-compose up
```

Frontend: http://localhost:3000
Backend API: http://localhost:8000
API docs: http://localhost:8000/docs

### Manual Setup

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Demo

```bash
cd backend
python examples/demo_predict.py
```

Upload any leaf photo at `/detect` to get disease, confidence, treatment, organic alternative, and probability breakdown.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/health | Health check |
| GET | /api/model-status | ML model status |
| POST | /api/predict | Single image detection |
| POST | /api/batch-predict | Batch upload (max 10) |
| GET | /api/crops | List 20+ crops |
| GET | /api/crops/{name} | Crop details |
| GET | /api/diseases | Disease encyclopedia |
| GET | /api/diseases/{name} | Disease detail |
| GET | /api/recommendations/rotation | Rotation plan |
| GET | /api/recommendations/fertilizer | Fertilizer calc |
| GET | /api/calendar/{crop} | Seasonal calendar |
| GET | /api/pesticides | Pesticide DB |
| GET | /api/market-prices/{crop} | Market price |
| GET | /api/pest-lifecycle/{pest} | Pest lifecycle |
| GET | /api/yield-prediction | Yield estimate |
| GET | /api/weather-advice | Farming advice |
| GET | /api/weather/irrigation-advice | Irrigation |
| GET | /api/weather/disease-risk | Risk forecast |
| GET | /api/weather/alerts | Alerts |

## ML Pipeline

- RGB to HSV custom conversion for illumination robustness
- Leaf segmentation with largest-component filtering
- Green / brown / yellow / dark-spot ratios
- Sobel edge density on leaf pixels
- 8-bin color histogram + GLCM contrast / homogeneity
- Profile matching across 10 diseases + softmax + margin calibration

## SIH Pitch

- Innovation: GPU-free CV that runs on a 500MB container, Tamil Nadu specific agronomy engine
- Impact: early detection saves 30 percent yield, organic options cut chemical cost
- Scalability: stateless FastAPI + file store, weather API pluggable, EN/TA ready for 70M Tamil speakers

## Tech Stack

- Backend: Python 3.12, FastAPI, Pillow, NumPy, SciPy, scikit-image, aiohttp
- Frontend: React 18, TypeScript, Vite, React Router
- Deployment: Docker Compose

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| OPENWEATHER_API_KEY | Weather API key | empty (rule-based fallback) |
| RATE_LIMIT_REQUESTS | Max requests per window | 100 |
| RATE_LIMIT_WINDOW | Window seconds | 60 |

## Running Tests

```bash
cd backend
pytest tests/ -v
```
