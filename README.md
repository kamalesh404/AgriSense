# AgriSense

[![CI](https://github.com/kamalesh404/agrisense/actions/workflows/ci.yml/badge.svg)](https://github.com/kamalesh404/agrisense/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![React](https://img.shields.io/badge/react-18-61dafb.svg)](https://react.dev/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

AI-powered crop disease detection and smart farming platform for Tamil Nadu farmers.

AgriSense combines GPU-free computer vision, a Tamil Nadu agronomy knowledge base, weather-aware decision support, and a bilingual farmer-friendly UI to help farmers detect disease early and act with confidence.

## Table of Contents

- [Problem Statement](#problem-statement)
- [Unique Solution](#unique-solution)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Demo](#demo)
- [API Reference](#api-reference)
- [ML Pipeline](#ml-pipeline)
- [SIH Pitch](#sih-pitch)
- [Environment Variables](#environment-variables)
- [Tests](#tests)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## Problem Statement

Farmers in Tamil Nadu lose 30-40% of crop yield every year to late disease detection, incorrect pesticide use, and limited access to agricultural experts.

A typical scenario: a smallholder farmer notices leaf spots, has no extension officer nearby, waits several days, sprays a broad-spectrum pesticide based on shop advice, and still loses a large portion of the crop. The loss is both yield and income, plus wasted chemical cost, water, and labor.

Existing solutions often require expensive hardware, GPU inference, English-only interfaces, or generic advice that does not match Tamil Nadu crops, seasons, soils, and disease pressure.

## Unique Solution

AgriSense is an offline-first, lightweight agricultural expert that runs in the browser:

- Real computer vision without a GPU, using HSV analysis, leaf segmentation, Sobel edges, GLCM texture, lesion ratios, and calibrated softmax scoring across 10 diseases.
- Tamil Nadu-first knowledge base with 20+ crops, disease lifecycles, pesticide database with dosage guidance, and organic alternatives for every major disease.
- Decision support beyond detection, including rotation planning, fertilizer calculation by soil and acreage, seasonal calendars, yield prediction, market prices, and weather-based irrigation and disease-risk advice.
- Farmer-centered UX with drag-and-drop batch upload, confidence gauge, treatment cards, disease encyclopedia, English/Tamil toggle, downloadable text report, and weather dashboard.
- Production guardrails including 10 MB upload limit, batch limit of 10 images, rate limiting, model-status endpoint, and full pytest coverage.

## Features

- 10-class crop disease detection with calibrated confidence scores
- Leaf segmentation with HSV, Sobel, and GLCM feature pipeline
- Single and batch prediction with probability breakdown
- Disease encyclopedia with search and filters
- 20+ crop database tailored to Tamil Nadu
- Crop rotation planner
- Fertilizer calculator by soil type and acreage
- Seasonal farming calendar per crop
- Yield prediction
- Market price lookup
- Pest lifecycle reference
- Weather irrigation advice, disease-risk forecast, and alerts
- English and Tamil UI with mobile-responsive layout
- Downloadable diagnosis report
- Docker Compose one-command demo

## Tech Stack

- Backend: Python 3.12, FastAPI, Pillow, NumPy, SciPy, scikit-image, aiohttp
- Frontend: React 18, TypeScript, Vite, React Router
- Testing: pytest for backend, TypeScript compiler and Vite build for frontend
- Deployment: Docker Compose
- CI: GitHub Actions

## Quick Start

### Prerequisites

- Docker and Docker Compose for container setup, or
- Python 3.12 and Node 20 for manual setup

### Run with Docker

```bash
docker-compose up --build
```

Open:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs

### Run Manually

Backend:

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm ci
npm run dev
```

The frontend runs at http://localhost:5173 by default in development and expects the backend at http://localhost:8000.

## Demo

Run the included prediction demo script:

```bash
cd backend
python examples/demo_predict.py
```

Then upload any leaf photo through the frontend Detect page or directly through the API:

```bash
curl -X POST http://localhost:8000/api/predict -F "file=@leaf.jpg"
```

Each prediction returns the detected disease, confidence score, treatment recommendation, organic alternative, and full probability breakdown.

## API Reference

Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| GET | `/api/health` | Service health check |
| GET | `/api/model-status` | ML model status and metadata |
| POST | `/api/predict` | Single-leaf disease prediction |
| POST | `/api/batch-predict` | Batch prediction, maximum 10 images |
| GET | `/api/crops` | List all supported crops |
| GET | `/api/crops/{name}` | Crop detail and agronomy guidance |
| GET | `/api/diseases` | Disease encyclopedia list |
| GET | `/api/diseases/{name}` | Disease detail, symptoms, and treatment |
| GET | `/api/recommendations/rotation` | Crop rotation plan |
| GET | `/api/recommendations/fertilizer` | Fertilizer calculation by soil and acreage |
| GET | `/api/calendar/{crop}` | Seasonal calendar for a crop |
| GET | `/api/pesticides` | Pesticide database with dosage |
| GET | `/api/market-prices/{crop}` | Market price for a crop |
| GET | `/api/pest-lifecycle/{pest}` | Pest lifecycle information |
| GET | `/api/yield-prediction` | Yield estimate by crop and acreage |
| GET | `/api/weather-advice` | General weather-based farming advice |
| GET | `/api/weather/irrigation-advice` | Irrigation recommendation |
| GET | `/api/weather/disease-risk` | Fungal and disease-risk forecast |
| GET | `/api/weather/alerts` | Active weather alerts |

Full interactive documentation is available at `/docs` when the backend is running.

## ML Pipeline

The AgriSense vision pipeline is designed to run on CPU in a lightweight container:

1. RGB to HSV conversion for illumination-robust color analysis.
2. Leaf segmentation with green masking and largest-component filtering to remove background.
3. Lesion quantification using green, brown, yellow, and dark-spot pixel ratios.
4. Sobel edge density computed on leaf pixels to capture blight, spot boundaries, and necrosis texture.
5. Color histogram with 8 bins per channel plus GLCM contrast and homogeneity for texture characterization.
6. Profile matching across 10 disease signatures, followed by softmax scoring and margin-based calibration.
7. Low-confidence and non-leaf guardrails that return cautious results instead of false certainty.

No GPU is required. The pipeline runs in a standard Python container with Pillow, NumPy, SciPy, and scikit-image.

## SIH Pitch

### Innovation

GPU-free computer vision that runs in a small container, combined with a Tamil Nadu-specific agronomy engine covering crops, diseases, pesticides, rotation, fertilizer, calendar, yield, market, and weather risk in one system.

### Impact

Early detection can prevent a large share of the 30-40% yield loss caused by late or incorrect treatment. Organic alternatives and precise dosage guidance reduce chemical cost and environmental harm. Tamil language support makes expert advice accessible to smallholder farmers.

### Scalability

Stateless FastAPI backend with file-based knowledge store, pluggable weather provider with rule-based fallback, and English/Tamil UI ready for millions of Tamil-speaking farmers. The architecture extends to additional crops, languages, and states without model retraining infrastructure.

## Environment Variables

| Variable | Description | Default |
| -------- | ----------- | ------- |
| `OPENWEATHER_API_KEY` | OpenWeather API key for live weather data | Empty, uses rule-based fallback |
| `RATE_LIMIT_REQUESTS` | Maximum requests per rate-limit window | `100` |
| `RATE_LIMIT_WINDOW` | Rate-limit window in seconds | `60` |
| `PYTHONUNBUFFERED` | Python container log behavior | `1` |

Copy `.env.example` to `.env` if present, or export variables before starting the backend.

## Tests

Backend:

```bash
cd backend
python -m pytest tests/ -v
```

Frontend:

```bash
cd frontend
npm ci
npx tsc --noEmit
npm run build
```

CI runs backend compile checks and pytest on Python 3.12, plus TypeScript checking and production build on Node 20, for every push and pull request to `main`.

## Roadmap

- Expand disease coverage beyond the initial 10 classes
- Add more Tamil Nadu and pan-India crops
- Improve calibration with field-collected validation data
- Offline mobile packaging for low-connectivity villages
- Voice input and image-based Tamil guidance
- Integration with soil-health card and mandi price feeds
- Multi-season advisory memory per farm

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for fork, branch, Conventional Commits, test, image data, and pull request guidance.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

See [SECURITY.md](SECURITY.md) for supported versions and vulnerability reporting. Report security issues to kamaleshorbit@gmail.com.

AgriSense provides informational pesticide, fertilizer, and agronomy guidance only and is not a substitute for professional agricultural advice. Always follow product labels and local regulations.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

Copyright 2026 Kamalesh (kamalesh404).
