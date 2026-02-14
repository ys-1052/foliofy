"""Tests for stock service."""

from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from app.services.stock_service import (
    StockAPIError,
    StockNotFoundError,
    get_multiple_prices,
    get_stock_price,
)


def test_get_stock_price_success():
    """Test successful stock price fetch."""
    import pandas as pd

    mock_ticker = MagicMock()
    # Create a real pandas DataFrame with 2 days of data
    mock_hist = pd.DataFrame({"Close": [175.25, 180.50]})
    mock_ticker.history.return_value = mock_hist
    mock_ticker.info = {"longName": "Apple Inc."}

    with patch("app.services.stock_service.yf.Ticker", return_value=mock_ticker):
        result = get_stock_price("AAPL")

    assert result["current_price"] == Decimal("180.50")
    assert result["previous_close"] == Decimal("175.25")
    assert result["name"] == "Apple Inc."
    assert isinstance(result["daily_change_pct"], Decimal)


def test_get_stock_price_empty_history():
    """Test stock price fetch with empty history (invalid symbol)."""
    mock_ticker = MagicMock()
    mock_hist = MagicMock()
    mock_hist.empty = True
    mock_ticker.history.return_value = mock_hist

    with patch("app.services.stock_service.yf.Ticker", return_value=mock_ticker):
        with pytest.raises(StockNotFoundError):
            get_stock_price("INVALID")


def test_get_stock_price_api_error():
    """Test stock price fetch with API error."""
    mock_ticker = MagicMock()
    mock_ticker.history.side_effect = Exception("API Error")

    with patch("app.services.stock_service.yf.Ticker", return_value=mock_ticker):
        with pytest.raises(StockAPIError):
            get_stock_price("AAPL")


def test_get_stock_price_fallback_name():
    """Test stock price with fallback to symbol when name fetch fails."""
    import pandas as pd

    mock_ticker = MagicMock()
    mock_hist = pd.DataFrame({"Close": [175.25, 180.50]})
    mock_ticker.history.return_value = mock_hist
    mock_ticker.info = {}  # No name info

    with patch("app.services.stock_service.yf.Ticker", return_value=mock_ticker):
        result = get_stock_price("AAPL")

    assert result["name"] == "AAPL"  # Fallback to symbol


def test_get_multiple_prices_success():
    """Test fetching multiple stock prices."""
    import pandas as pd

    mock_ticker = MagicMock()
    mock_hist = pd.DataFrame({"Close": [175.25, 180.50]})
    mock_ticker.history.return_value = mock_hist
    mock_ticker.info = {"longName": "Test Stock"}

    with patch("app.services.stock_service.yf.Ticker", return_value=mock_ticker):
        result = get_multiple_prices(["AAPL", "GOOGL"])

    assert len(result) == 2
    assert "AAPL" in result
    assert "GOOGL" in result
    assert result["AAPL"] is not None
    assert result["GOOGL"] is not None


def test_get_multiple_prices_partial_failure():
    """Test fetching multiple prices with some failures."""

    def mock_get_stock_price(symbol):
        if symbol == "AAPL":
            return {
                "current_price": Decimal("180.00"),
                "previous_close": Decimal("175.00"),
                "daily_change_pct": Decimal("2.86"),
                "name": "Apple Inc.",
            }
        else:
            raise StockNotFoundError("Invalid symbol")

    with patch("app.services.stock_service.get_stock_price", side_effect=mock_get_stock_price):
        result = get_multiple_prices(["AAPL", "INVALID"])

    assert len(result) == 2
    assert result["AAPL"] is not None
    assert result["INVALID"] is None


def test_get_stock_price_single_day_history():
    """Test with only one day of history (use open as previous)."""
    import pandas as pd

    mock_ticker = MagicMock()
    # Create a real pandas DataFrame with one day
    mock_hist = pd.DataFrame({"Close": [180.50], "Open": [175.00]})
    mock_ticker.history.return_value = mock_hist
    mock_ticker.info = {"longName": "Test Stock"}

    with patch("app.services.stock_service.yf.Ticker", return_value=mock_ticker):
        result = get_stock_price("AAPL")

    assert result["current_price"] == Decimal("180.50")
    assert result["previous_close"] == Decimal("175.00")
