.PHONY: help install format format-check lint typecheck check test migrate migrate-auto upgrade downgrade run clean

# デフォルトターゲット: ヘルプを表示
help:
	@echo "Available commands:"
	@echo "  make install        - Install all dependencies"
	@echo "  make format         - Format code with black and ruff"
	@echo "  make format-check   - Check code formatting (CI)"
	@echo "  make lint           - Run linter (ruff)"
	@echo "  make typecheck      - Run type checker (mypy)"
	@echo "  make check          - Run all checks (lint + type check)"
	@echo "  make test           - Run tests with pytest"
	@echo "  make migrate-auto   - Generate migration automatically"
	@echo "  make upgrade        - Apply migrations"
	@echo "  make downgrade      - Rollback last migration"
	@echo "  make run            - Run development server"
	@echo "  make clean          - Clean cache files"

# 依存関係インストール
install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# コードフォーマット
format:
	@echo "🎨 Formatting code with black..."
	black app/ alembic/
	@echo "🎨 Sorting imports with ruff..."
	ruff check --select I --fix app/ alembic/
	@echo "✅ Formatting complete!"

# コードフォーマットチェック（CI用）
format-check:
	@echo "🎨 Checking code formatting with black..."
	black --check app/ alembic/
	@echo "🎨 Checking import sorting with ruff..."
	ruff check --select I app/ alembic/
	@echo "✅ Format check complete!"

# リンター実行
lint:
	@echo "🔍 Running ruff linter..."
	ruff check app/ alembic/
	@echo "✅ Linting complete!"

# 型チェック
typecheck:
	@echo "🔍 Running mypy type checker..."
	mypy app/
	@echo "✅ Type check complete!"

# 全チェック実行
check: lint typecheck
	@echo "✅ All checks passed!"

# テスト実行
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v
	@echo "✅ Tests complete!"

# マイグレーション自動生成
migrate-auto:
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"

# マイグレーション適用
upgrade:
	@echo "⬆️  Applying migrations..."
	alembic upgrade head
	@echo "✅ Migrations applied!"

# マイグレーションロールバック
downgrade:
	@echo "⬇️  Rolling back migration..."
	alembic downgrade -1
	@echo "✅ Migration rolled back!"

# 開発サーバー起動
run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# キャッシュクリーンアップ
clean:
	@echo "🧹 Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"
