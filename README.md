# Foliofy - 保有株管理ツール

米国株の保有資産を視覚化・管理するWebアプリケーション

## Tech Stack

- **Backend**: FastAPI + Python 3.11 + PostgreSQL
- **Frontend**: Next.js 14 + React + TypeScript
- **Infrastructure**: Docker + Docker Compose

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository
```bash
git clone <repository-url>
cd foliofy
```

2. Start Docker containers
```bash
docker-compose up -d
```

3. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Development

Stop containers:
```bash
docker-compose down
```

View logs:
```bash
docker-compose logs -f
```

Rebuild containers:
```bash
docker-compose up -d --build
```

## Project Structure

```
foliofy/
├── backend/          # FastAPI application
├── frontend/         # Next.js application
├── docker-compose.yml
└── README.md
```

## Features (MVP)

- ✅ 保有株登録（米国株のみ）
- ✅ ダッシュボード
  - ヒートマップ（色=当日騰落率、面積=評価額）
  - 円グラフ（資産配分）
- ✅ 認証（Cognito）
