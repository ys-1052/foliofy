# Git規則

## コミットメッセージの接頭語

- `add` - 新規ファイル・機能の追加
- `update` - 既存機能の更新・改善
- `fix` - バグ修正
- `refactor` - リファクタリング
- `docs` - ドキュメント更新
- `test` - テスト追加・修正
- `chore` - 雑務（依存関係更新、設定変更など）

**例:**
```
add user authentication API
update dashboard UI layout
fix login validation error
refactor database connection logic
docs: update API documentation
test: add holdings endpoint tests
chore: update dependencies to latest
```

## ブランチ命名規則

**フォーマット:** `<type>/<description-in-kebab-case>`

### タイプ

- `feature/` - 新機能開発
- `fix/` - バグ修正
- `refactor/` - リファクタリング
- `docs/` - ドキュメント更新
- `test/` - テスト追加
- `chore/` - 雑務

### 命名ルール

- 小文字のみ
- 単語区切りはハイフン（kebab-case）
- 簡潔で説明的（最大50文字）

**例:**
```
feature/user-authentication
feature/dashboard-heatmap
fix/login-validation-error
fix/api-response-format
refactor/database-models
docs/api-endpoints
test/holdings-crud
chore/update-dependencies
```

## Co-Authoredタグ

全てのコミットに以下を付与（モデル名は実行時のものを使用）：
```
Co-Authored-By: Claude <model-name> <noreply@anthropic.com>
```
