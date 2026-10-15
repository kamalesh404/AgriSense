# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x     | Yes                |
| 1.x     | Security fixes only |
| < 1.0   | No                 |

We recommend running the latest release of AgriSense. Older versions may not receive security updates.

## Reporting a Vulnerability

To report a security vulnerability, email kamaleshorbit@gmail.com with:

- A description of the vulnerability and its potential impact
- Steps to reproduce the issue
- Affected version, commit hash, or deployment details
- Any relevant logs, screenshots, or proof-of-concept details

We will acknowledge receipt within 3 business days and provide a remediation timeline after initial assessment. Please allow reasonable time for a fix before public disclosure.

Please do not open public GitHub issues for suspected security vulnerabilities.

## Scope

In scope:

- Backend API in `backend/`, including authentication, upload handling, rate limiting, and prediction endpoints
- Frontend application in `frontend/`, including data handling and API interaction
- Docker and deployment configuration in `docker-compose.yml` and related Dockerfiles
- Dependencies declared in `backend/requirements.txt` and `frontend/package.json`

Out of scope:

- Third-party services such as weather providers
- User-hosted infrastructure misconfigurations
- Social engineering or physical attacks

## Pesticide and Agronomy Safety Note

AgriSense provides informational pesticide, fertilizer, and agronomy guidance only. It is not a substitute for professional agricultural advice. Users must follow local regulations, product labels, and guidance from qualified agricultural officers. The maintainers accept no liability for pesticide misuse, incorrect dosage, crop damage, health effects, or environmental harm resulting from use of this software.

## Disclosure Policy

Once a vulnerability is fixed, we will publish a security advisory and include the fix in the [CHANGELOG](CHANGELOG.md). Reporters will be credited if they wish.
