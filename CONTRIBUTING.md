# Contributing to AgriSense

Thank you for your interest in contributing to AgriSense. This guide explains how to set up your environment, follow project conventions, and submit changes.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Branching](#branching)
- [Commit Messages](#commit-messages)
- [Development Setup](#development-setup)
- [Running Checks](#running-checks)
- [Image Test Data Guidance](#image-test-data-guidance)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

By participating in this project you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:

   ```bash
   git clone https://github.com/<your-username>/agrisense.git
   cd agrisense
   ```

3. Add the upstream remote:

   ```bash
   git remote add upstream https://github.com/kamalesh404/agrisense.git
   git fetch upstream
   ```

## How to Contribute

- Report bugs using the bug report issue template.
- Suggest features using the feature request issue template with farmer impact described.
- Fix open issues, improve documentation, add tests, or extend crop and disease coverage.
- For large changes, open an issue first to discuss scope and design.

## Branching

- Create a feature branch from `main` for every change.
- Use short, descriptive branch names:

  ```bash
  git checkout -b feat/rotation-planner
  git checkout -b fix/predict-confidence
  git checkout -b docs/api-table
  ```

- Recommended prefixes: `feat/`, `fix/`, `docs/`, `chore/`, `test/`, `refactor/`.
- Keep branches focused on a single issue or feature.
- Rebase or merge `main` regularly to avoid large conflicts.

## Commit Messages

This project uses Conventional Commits. Format:

```text
type(scope): short summary
```

Common types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `perf`, `ci`.

Examples:

```text
feat(api): add batch-predict endpoint limit handling
fix(ml): correct softmax calibration for low-confidence cases
docs(readme): update quick start instructions
test(backend): add rotation planner coverage
```

Write commit subjects in imperative mood, keep them under 72 characters, and add a body when the change needs context.

## Development Setup

Backend (Python 3.12):

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend (Node 20):

```bash
cd frontend
npm ci
npm run dev
```

Docker (full stack):

```bash
docker-compose up --build
```

## Running Checks

Run these checks before opening a pull request.

Backend:

```bash
cd backend
python -m compileall app
python -m pytest tests/ -v
```

Frontend:

```bash
cd frontend
npm ci
npx tsc --noEmit
npm run build
```

All checks must pass. Add or update tests for bug fixes and new features.

## Image Test Data Guidance

Disease-detection changes often require image fixtures. Follow these rules:

- Do not commit copyrighted, personal, or farm-identifiable images.
- Prefer synthetic or openly licensed leaf images with clear attribution where required.
- Keep fixtures small; resize test images to the minimum size that reproduces the case.
- Place backend fixtures under `backend/tests/data/` with descriptive names such as `healthy-leaf.jpg` or `blight-sample.jpg`.
- Document image source, license, crop, and expected prediction in the related test or PR description.
- Never commit images larger than 2 MB. Production uploads are limited to 10 MB and batch prediction accepts a maximum of 10 images.

## Pull Request Process

1. Sync your branch with upstream `main`.
2. Run backend and frontend checks listed above.
3. Push your branch to your fork and open a pull request against `main`.
4. Fill out the pull request template completely, including summary, tests, and farmer impact.
5. Link related issues using `Fixes #<issue-number>` where applicable.
6. Request review and respond to feedback. Keep the pull request focused; split unrelated changes.
7. Maintainers will squash-merge after approval and passing CI.

Thank you for helping Tamil Nadu farmers with reliable, practical tooling.
