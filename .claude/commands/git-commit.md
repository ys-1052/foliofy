# git-commit

Gitコミットを作成してpushする

**参照:** `.claude/skills/git-conventions.md`のコミットメッセージ規則に従う

## 実行手順

1. **ステージング状態を確認**
   ```bash
   git status
   git diff --cached
   git log --oneline -5
   ```
   - ステージング済みファイルがなければ何もせず終了

2. **変更を分析してメッセージ作成**
   - git-conventions.mdの接頭語ルールに従う
   - 簡潔に「何をしたか」を1-2行で記述

3. **コミット & Push**
   ```bash
   git commit -m "$(cat <<'EOF'
   <prefix> <message>

   Co-Authored-By: Claude <current-model> <noreply@anthropic.com>
   EOF
   )"
   git push
   ```

   **Note:** `<current-model>` は実行時のモデル名に置き換える

## 注意事項

- **ステージング済みファイルのみ**をコミット対象とする
