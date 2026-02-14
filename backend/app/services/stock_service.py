"""Stock price service using yfinance API.

Note:
    Yahoo Finance API (yfinance) can be rate-limited or unstable at times.
    For production use, consider:
    - Alpha Vantage API
    - IEX Cloud API
    - Polygon.io API
    - Finnhub API

    The implementation handles errors gracefully and can be easily swapped
    with another API provider.
"""

import logging
from decimal import Decimal
from typing import Any

import yfinance as yf

logger = logging.getLogger(__name__)


class StockServiceError(Exception):
    """Base exception for stock service errors."""

    pass


class StockNotFoundError(StockServiceError):
    """Raised when stock symbol is not found."""

    pass


class StockAPIError(StockServiceError):
    """Raised when yfinance API fails."""

    pass


def get_stock_price(symbol: str) -> dict[str, Any]:
    """
    Fetch current stock price and related data from yfinance.

    Args:
        symbol: Stock symbol (e.g., "AAPL", "GOOGL")

    Returns:
        Dictionary containing:
            - current_price: Current stock price
            - previous_close: Previous day's closing price
            - daily_change_pct: Daily change percentage
            - name: Company name

    Raises:
        StockNotFoundError: If symbol is invalid or not found
        StockAPIError: If API request fails
    """
    try:
        ticker = yf.Ticker(symbol)

        # Use history() instead of info for more reliable data
        # Get last 2 days of data
        hist = ticker.history(period="2d")

        if hist.empty or len(hist) < 1:
            logger.warning(f"Stock symbol not found or no data: {symbol}")
            raise StockNotFoundError(f"Stock symbol '{symbol}' not found")

        # Get current price (latest close) and previous close
        current_price_raw = hist["Close"].iloc[-1]

        if len(hist) >= 2:
            previous_close_raw = hist["Close"].iloc[-2]
        else:
            # If only 1 day available, use open price as previous close
            previous_close_raw = hist["Open"].iloc[-1]

        # Convert to Decimal for precision
        current_price = Decimal(str(round(current_price_raw, 2)))
        previous_close = Decimal(str(round(previous_close_raw, 2)))

        # Calculate daily change percentage
        if previous_close > 0:
            daily_change_pct = ((current_price - previous_close) / previous_close) * 100
        else:
            daily_change_pct = Decimal(0)

        # Try to get company name from info (fallback to symbol)
        try:
            info = ticker.info
            name = info.get("longName") or info.get("shortName") or symbol
        except Exception:
            # If info fails, just use symbol as name
            name = symbol

        logger.info(f"Fetched price for {symbol}: ${current_price}")

        return {
            "current_price": current_price,
            "previous_close": previous_close,
            "daily_change_pct": daily_change_pct,
            "name": name,
        }

    except (StockNotFoundError, StockAPIError):
        # Re-raise our custom exceptions
        raise
    except Exception as e:
        logger.exception(f"Unexpected error fetching stock data for {symbol}: {e}")
        raise StockAPIError(f"Failed to fetch data for '{symbol}': {str(e)}") from e


def get_multiple_prices(symbols: list[str]) -> dict[str, dict[str, Any] | None]:
    """
    Fetch prices for multiple stocks (batch operation).

    Args:
        symbols: List of stock symbols

    Returns:
        Dictionary mapping symbol to price data (or None if fetch failed)
    """
    results: dict[str, dict[str, Any] | None] = {}
    for symbol in symbols:
        try:
            results[symbol] = get_stock_price(symbol)
        except (StockNotFoundError, StockAPIError) as e:
            logger.warning(f"Failed to fetch price for {symbol}: {e}")
            results[symbol] = None

    return results
