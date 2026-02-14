"""Tests for dashboard API."""

from decimal import Decimal
from unittest.mock import patch


def test_dashboard_no_holdings(client, test_user):
    """Test dashboard with no holdings."""
    response = client.get("/dashboard")
    assert response.status_code == 404
    assert "No holdings found" in response.json()["detail"]


def test_dashboard_with_holdings(client, test_user):
    """Test dashboard with holdings."""
    # Mock stock prices
    def mock_get_multiple_prices(symbols):
        prices = {
            "AAPL": {
                "current_price": Decimal("180.00"),
                "previous_close": Decimal("175.00"),
                "daily_change_pct": Decimal("2.86"),
                "name": "Apple Inc.",
            },
            "GOOGL": {
                "current_price": Decimal("2900.00"),
                "previous_close": Decimal("2850.00"),
                "daily_change_pct": Decimal("1.75"),
                "name": "Alphabet Inc.",
            },
        }
        return {symbol: prices.get(symbol) for symbol in symbols}

    # Create holdings
    with patch("app.routers.holdings.get_stock_price") as mock_get_price:
        mock_get_price.side_effect = [
            {
                "current_price": Decimal("180.00"),
                "previous_close": Decimal("175.00"),
                "daily_change_pct": Decimal("2.86"),
                "name": "Apple Inc.",
            },
            {
                "current_price": Decimal("2900.00"),
                "previous_close": Decimal("2850.00"),
                "daily_change_pct": Decimal("1.75"),
                "name": "Alphabet Inc.",
            },
        ]
        client.post("/holdings", json={"symbol": "AAPL", "shares": 10, "avg_cost": 150.00})
        client.post("/holdings", json={"symbol": "GOOGL", "shares": 2, "avg_cost": 2800.00})

    # Get dashboard
    with patch("app.routers.dashboard.get_multiple_prices", side_effect=mock_get_multiple_prices):
        response = client.get("/dashboard")

    assert response.status_code == 200
    data = response.json()

    # Verify structure
    assert "total_value" in data
    assert "total_cost" in data
    assert "total_pnl" in data
    assert "total_pnl_pct" in data
    assert "holdings" in data
    assert len(data["holdings"]) == 2

    # Verify calculations
    # AAPL: 10 shares @ 150 cost, 180 current = 1800 value, 300 pnl
    # GOOGL: 2 shares @ 2800 cost, 2900 current = 5800 value, 200 pnl
    # Total: 7600 value, 7100 cost, 500 pnl, 7.04% pnl_pct

    total_value = Decimal(str(data["total_value"]))
    total_cost = Decimal(str(data["total_cost"]))
    total_pnl = Decimal(str(data["total_pnl"]))

    assert total_value == Decimal("7600.00")
    assert total_cost == Decimal("7100.00")
    assert total_pnl == Decimal("500.00")

    # Verify holdings details
    aapl_holding = next(h for h in data["holdings"] if h["symbol"] == "AAPL")
    assert Decimal(str(aapl_holding["market_value"])) == Decimal("1800.00")
    assert Decimal(str(aapl_holding["pnl"])) == Decimal("300.00")
    assert Decimal(str(aapl_holding["pnl_pct"])) == Decimal("20.00")

    # Verify allocation percentages (AAPL: 1800/7600 = 23.68%)
    aapl_allocation = Decimal(str(aapl_holding["allocation_pct"]))
    expected_allocation = Decimal("23.68")
    assert abs(aapl_allocation - expected_allocation) < Decimal("0.01")


def test_dashboard_price_fetch_failure(client, test_user):
    """Test dashboard when all price fetches fail."""

    def mock_get_multiple_prices_fail(symbols):
        return {symbol: None for symbol in symbols}

    # Create holding
    with patch("app.routers.holdings.get_stock_price") as mock_get_price:
        mock_get_price.return_value = {
            "current_price": Decimal("180.00"),
            "previous_close": Decimal("175.00"),
            "daily_change_pct": Decimal("2.86"),
            "name": "Apple Inc.",
        }
        client.post("/holdings", json={"symbol": "AAPL", "shares": 10, "avg_cost": 150.00})

    # Get dashboard with failed price fetch
    with patch(
        "app.routers.dashboard.get_multiple_prices", side_effect=mock_get_multiple_prices_fail
    ):
        response = client.get("/dashboard")

    assert response.status_code == 503
    assert "Unable to fetch stock prices" in response.json()["detail"]


def test_dashboard_partial_price_fetch(client, test_user):
    """Test dashboard when some price fetches fail."""

    def mock_get_multiple_prices_partial(symbols):
        prices = {
            "AAPL": {
                "current_price": Decimal("180.00"),
                "previous_close": Decimal("175.00"),
                "daily_change_pct": Decimal("2.86"),
                "name": "Apple Inc.",
            },
            "GOOGL": None,  # Failed to fetch
        }
        return {symbol: prices.get(symbol) for symbol in symbols}

    # Create holdings
    with patch("app.routers.holdings.get_stock_price") as mock_get_price:
        mock_get_price.side_effect = [
            {
                "current_price": Decimal("180.00"),
                "previous_close": Decimal("175.00"),
                "daily_change_pct": Decimal("2.86"),
                "name": "Apple Inc.",
            },
            {
                "current_price": Decimal("2900.00"),
                "previous_close": Decimal("2850.00"),
                "daily_change_pct": Decimal("1.75"),
                "name": "Alphabet Inc.",
            },
        ]
        client.post("/holdings", json={"symbol": "AAPL", "shares": 10, "avg_cost": 150.00})
        client.post("/holdings", json={"symbol": "GOOGL", "shares": 2, "avg_cost": 2800.00})

    # Get dashboard - should only include AAPL
    with patch(
        "app.routers.dashboard.get_multiple_prices", side_effect=mock_get_multiple_prices_partial
    ):
        response = client.get("/dashboard")

    assert response.status_code == 200
    data = response.json()
    assert len(data["holdings"]) == 1
    assert data["holdings"][0]["symbol"] == "AAPL"
