# Services

ビジネスロジックを実装するサービス層

## stock_service.py

株価データ取得サービス（yfinance使用）

### 使用方法

```python
from app.services.stock_service import get_stock_price, StockNotFoundError, StockAPIError

try:
    data = get_stock_price("AAPL")
    print(f"Price: ${data['current_price']}")
    print(f"Daily Change: {data['daily_change_pct']}%")
except StockNotFoundError:
    print("Symbol not found")
except StockAPIError as e:
    print(f"API error: {e}")
```

### ⚠️ 注意事項

**Yahoo Finance API (yfinance) の制限:**
- レート制限がある（429 Too Many Requests）
- 不安定な場合がある
- 本番環境では有料APIの検討を推奨

**本番環境での代替API:**
- [Alpha Vantage](https://www.alphavantage.co/) - 無料枠あり
- [IEX Cloud](https://iexcloud.io/) - リアルタイムデータ
- [Polygon.io](https://polygon.io/) - 高速・安定
- [Finnhub](https://finnhub.io/) - 無料枠あり

### 実装詳細

**データソース:**
- `ticker.history(period="2d")` を使用（infoより安定）
- 最新の終値を現在価格として使用
- 前日終値との差分で騰落率を計算

**エラーハンドリング:**
- `StockNotFoundError`: 無効なシンボル
- `StockAPIError`: API呼び出し失敗
- ログ出力で詳細を記録

### 将来の改善案

1. **キャッシング**: Redisで価格データをキャッシュ（5-15分）
2. **リトライ**: exponential backoffでリトライ
3. **フォールバック**: 複数のAPIプロバイダーに対応
4. **WebSocket**: リアルタイム価格更新
