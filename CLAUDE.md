# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Language Rules

- All code, comments, docstrings, error messages, and UI text must be in **English**.
- Git commit messages must be in English.
- Respond to the user in Japanese, but all generated code must be in English.

## Development Commands

```bash
# Docker
docker-compose up -d
docker-compose up -d --build frontend
docker-compose exec backend alembic upgrade head

# Backend (Python 3.13, inside Docker)
docker-compose exec backend make check       # lint + typecheck
docker-compose exec backend make test        # pytest
docker-compose exec backend make format      # black + ruff

# Frontend (Node 22, inside Docker or local)
npm run check                                # lint + typecheck + format:check
npm run build
npm run format

# AWS CDK
cd aws && npm run synth
```

## CI

Always verify locally before pushing:
- Backend: `make check && make test`
- Frontend: `npm run check && npm run build`
