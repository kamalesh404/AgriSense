# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-10-01

### Added

- 10-disease computer vision pipeline with HSV conversion, leaf segmentation, Sobel edge density, GLCM texture, lesion ratios, and softmax calibration
- Crop database covering 20+ Tamil Nadu crops with details, seasons, and agronomy guidance
- Crop rotation planner endpoint with rotation recommendations
- Fertilizer calculator by soil type and acreage
- Seasonal farming calendar per crop
- Yield prediction endpoint with acreage and crop-based estimates
- Market price lookup per crop
- Pest lifecycle reference endpoint
- Weather risk engine with irrigation advice, disease-risk forecast, and alerts
- Batch prediction for up to 10 images with 10 MB per-image limit
- English and Tamil UI with language toggle and mobile-responsive farmer UX
- Treatment cards with pesticide dosage and organic alternatives
- Downloadable text report and confidence gauge in frontend
- Disease encyclopedia with search and filters
- Model status endpoint, rate limiting, and full pytest suite

### Changed

- Reworked prediction scoring with margin-based calibration
- Improved leaf segmentation with largest-component filtering
- Expanded API documentation and Docker Compose demo workflow

### Fixed

- Handling of low-confidence and non-leaf uploads
- Validation for oversized images and oversized batches

## [1.0.0] - 2026-06-15

### Added

- Initial FastAPI backend with health check and single-image prediction
- React 18 with TypeScript and Vite frontend
- Basic crop and disease reference endpoints
- Docker Compose setup for backend and frontend
- Backend pytest coverage for core endpoints
