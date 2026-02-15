# Foliofy - 保有株管理ツール

米国株の保有資産を視覚化・管理するWebアプリケーション

## Features

- 保有株の登録・編集・削除
- ポートフォリオダッシュボード
  - 評価額・損益サマリー
  - ヒートマップ（面積=評価額、色=騰落率）
  - 資産配分パイチャート
- リアルタイム株価取得

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

