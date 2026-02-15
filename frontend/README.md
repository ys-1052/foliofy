# Foliofy Frontend

Next.js + React による保有株管理ツールのフロントエンド

## Tech Stack

- Next.js + React + TypeScript
- TailwindCSS (Styling)
- Recharts (Charts)
- ESLint + Prettier (Linting & Formatting)

## Setup

```bash
# Start containers
docker-compose up -d
```

Access: http://localhost:3000

## Development

```bash
# Format code
docker-compose exec frontend npm run format

# Lint & Type Check
docker-compose exec frontend npm run check

# Build for production
docker-compose exec frontend npm run build
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier
- `npm run typecheck` - Run TypeScript type check
- `npm run check` - Run all checks (lint + typecheck + format)
