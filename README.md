# Foliofy - Stock Portfolio Manager

A web application for visualizing and managing US stock holdings.

## Features

- Add, edit, and delete stock holdings
- Portfolio dashboard
  - Market value and P&L summary
  - Heatmap (area = market value, color = daily change)
  - Asset allocation pie chart
- Real-time stock price fetching

## Tech Stack

- **Backend**: FastAPI + Python + PostgreSQL
- **Frontend**: Next.js + React + TypeScript
- **Infrastructure**: Docker

## Getting Started

### Prerequisites

- Docker Desktop

### Setup

```bash
# Clone the repository
git clone https://github.com/ys-1052/foliofy.git
cd foliofy

# Start containers
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head
```

### Access

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Development

```bash
# Backend: Format & Lint & Test
docker-compose exec backend make check
docker-compose exec backend make test

# Frontend: Format & Lint & Type Check
docker-compose exec frontend npm run check

# View logs
docker-compose logs -f
```
