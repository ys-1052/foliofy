# Foliofy Backend

FastAPI + Python による保有株管理ツールのバックエンドAPI

## Tech Stack

- FastAPI + Python + PostgreSQL
- SQLAlchemy (ORM)
- Alembic (Migration)
- yfinance (Stock API)
- Pytest (Testing)

## Setup

```bash
# Start containers
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head
```

## Development

```bash
# Format & Lint & Type Check
docker-compose exec backend make check

# Run tests
docker-compose exec backend make test

# Generate migration
docker-compose exec backend make migrate-auto

# Apply migration
docker-compose exec backend make upgrade
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Available Make Commands

Run `make help` to see all available commands.
