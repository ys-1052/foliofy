# Foliofy Backend

FastAPI + Python 3.13 による保有株管理ツールのバックエンドAPI

## 📦 技術スタック

- **FastAPI** 0.115.6 - Webフレームワーク
- **SQLAlchemy** 2.0.36 - ORM
- **PostgreSQL** 15 - データベース
- **Alembic** 1.14.0 - マイグレーション
- **yfinance** 0.2.50 - 株価データ取得
- **Pydantic** 2.10.3 - データバリデーション

### 開発ツール

- **Black** 24.10.0 - コードフォーマッター
- **Ruff** 0.8.4 - 高速リンター
- **Mypy** 1.13.0 - 型チェッカー
- **Pytest** 8.3.4 - テストフレームワーク

## 🚀 セットアップ

### Docker環境（推奨）

```bash
# コンテナ起動
docker-compose up -d

# マイグレーション適用
docker-compose exec backend make upgrade

# ログ確認
docker-compose logs -f backend
```

### ローカル環境

```bash
cd backend

# 依存関係インストール
make install

# マイグレーション適用
make upgrade

# 開発サーバー起動
make run
```

## 📝 Makeコマンド

### コード品質

```bash
# コードフォーマット（black + ruff）
make format

# リンター実行
make lint

# 型チェック
make typecheck

# 全チェック（lint + typecheck）
make check
```

### データベース

```bash
# マイグレーション自動生成
make migrate-auto

# マイグレーション適用
make upgrade

# マイグレーションロールバック（1つ戻す）
make downgrade
```

### テスト

```bash
# テスト実行
make test
```

### その他

```bash
# ヘルプ表示
make help

# キャッシュクリーンアップ
make clean

# 開発サーバー起動
make run
```

## 🐳 Docker環境での使用

```bash
# コンテナ内でmakeコマンド実行
docker-compose exec backend make format
docker-compose exec backend make lint
docker-compose exec backend make check
docker-compose exec backend make test
```

## 🗄️ データベース

### マイグレーション

```bash
# 自動生成（モデル変更を検出）
docker-compose exec backend make migrate-auto
# または
docker-compose exec backend alembic revision --autogenerate -m "メッセージ"

# 適用
docker-compose exec backend make upgrade

# ロールバック
docker-compose exec backend make downgrade
```

### 直接アクセス

```bash
# PostgreSQL CLIで接続
docker-compose exec db psql -U postgres -d foliofy

# テーブル一覧
\dt

# テーブル構造確認
\d users
\d holdings
```

## 📂 プロジェクト構造

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPIアプリケーション
│   ├── database.py       # DB接続設定
│   ├── models.py         # SQLAlchemyモデル
│   ├── schemas.py        # Pydanticスキーマ
│   ├── routers/          # APIエンドポイント
│   └── services/         # ビジネスロジック
├── alembic/              # マイグレーション
│   ├── versions/         # マイグレーションファイル
│   ├── env.py           # Alembic環境設定
│   └── script.py.mako   # テンプレート
├── tests/               # テストコード
├── Makefile             # 開発コマンド
├── pyproject.toml       # ツール設定
├── requirements.txt     # 本番依存関係
├── requirements-dev.txt # 開発依存関係
└── Dockerfile
```

## 🧪 テスト

```bash
# すべてのテスト実行
make test

# 特定のテストファイル
pytest tests/test_holdings.py -v

# カバレッジ付き
pytest --cov=app tests/
```

## 🎨 コーディング規約

### フォーマット

- **Black**: 行長100文字、Python 3.13
- **Ruff**: importの自動ソート

### リンター

有効なルール:
- `E/W`: pycodestyle（PEP8準拠）
- `F`: pyflakes（未使用変数など）
- `I`: isort（import順序）
- `N`: pep8-naming（命名規則）
- `UP`: pyupgrade（新しいPython構文）
- `B`: flake8-bugbear（バグ検出）
- `C4`: flake8-comprehensions（内包表記最適化）

### 型チェック

- Mypy使用
- Python 3.13の型アノテーション必須
- 外部ライブラリの型エラーは無視設定済み

## 🔧 開発ワークフロー

### 1. 機能開発

```bash
# ブランチ作成
git checkout -b feature/新機能

# コード編集
vim app/routers/holdings.py

# フォーマット
make format

# チェック
make check
```

### 2. モデル変更

```bash
# モデル編集
vim app/models.py

# マイグレーション生成
make migrate-auto

# 適用
make upgrade

# テスト
make test
```

### 3. コミット前

```bash
# 全チェック実行
make check

# テスト実行
make test

# キャッシュクリーンアップ
make clean
```

## 📚 API ドキュメント

開発サーバー起動後:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🐛 トラブルシューティング

### マイグレーションエラー

```bash
# 現在のバージョン確認
docker-compose exec backend alembic current

# 履歴確認
docker-compose exec backend alembic history

# 強制的にリセット（開発環境のみ）
docker-compose down -v
docker-compose up -d
docker-compose exec backend make upgrade
```

### リンターエラー

```bash
# 自動修正可能なエラーを修正
docker-compose exec backend ruff check --fix app/

# フォーマット実行
docker-compose exec backend make format
```

### 型エラー

```bash
# 詳細な型チェック
docker-compose exec backend mypy app/ --show-error-codes

# 特定ファイルのみ
docker-compose exec backend mypy app/models.py
```
