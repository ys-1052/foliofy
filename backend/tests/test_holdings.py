"""Tests for holdings CRUD API."""

from decimal import Decimal
from unittest.mock import patch

import pytest


def test_list_holdings_empty(client, test_user):
    """Test getting empty holdings list."""
    response = client.get("/holdings")
    assert response.status_code == 200
    assert response.json() == []


def test_create_holding(client, test_user):
    """Test creating a new holding."""
    mock_stock_data = {
        "current_price": Decimal("180.00"),
        "previous_close": Decimal("175.00"),
        "daily_change_pct": Decimal("2.86"),
        "name": "Apple Inc.",
    }

    with patch("app.routers.holdings.get_stock_price", return_value=mock_stock_data):
        response = client.post(
            "/holdings", json={"symbol": "AAPL", "shares": 10, "avg_cost": 150.00}
        )

    assert response.status_code == 201
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["name"] == "Apple Inc."
    assert Decimal(str(data["shares"])) == Decimal("10.00")
    assert Decimal(str(data["avg_cost"])) == Decimal("150.00")
    assert "id" in data
    assert "created_at" in data


def test_create_holding_weighted_average(client, test_user):
    """Test creating a holding with weighted average calculation."""
    mock_stock_data = {
        "current_price": Decimal("180.00"),
        "previous_close": Decimal("175.00"),
        "daily_change_pct": Decimal("2.86"),
        "name": "Apple Inc.",
    }

    with patch("app.routers.holdings.get_stock_price", return_value=mock_stock_data):
        # First purchase: 10 shares @ $150
        response1 = client.post(
            "/holdings", json={"symbol": "AAPL", "shares": 10, "avg_cost": 150.00}
        )
        assert response1.status_code == 201

        # Second purchase: 5 shares @ $160
        response2 = client.post(
            "/holdings", json={"symbol": "AAPL", "shares": 5, "avg_cost": 160.00}
        )
        assert response2.status_code == 201

    # Verify weighted average: (10*150 + 5*160) / 15 = 153.33
    data = response2.json()
    assert Decimal(str(data["shares"])) == Decimal("15.00")
    expected_avg = Decimal("153.33")
    actual_avg = Decimal(str(data["avg_cost"]))
    assert abs(actual_avg - expected_avg) < Decimal("0.01")


def test_create_holding_invalid_symbol(client, test_user):
    """Test creating a holding with invalid symbol."""
    from app.services.stock_service import StockNotFoundError

    with patch(
        "app.routers.holdings.get_stock_price", side_effect=StockNotFoundError("Invalid symbol")
    ):
        response = client.post(
            "/holdings", json={"symbol": "INVALID", "shares": 10, "avg_cost": 100.00}
        )

    assert response.status_code == 400
    assert "Invalid stock symbol" in response.json()["detail"]


def test_list_holdings_with_data(client, test_user):
    """Test listing holdings after creating some."""
    mock_stock_data = {
        "current_price": Decimal("180.00"),
        "previous_close": Decimal("175.00"),
        "daily_change_pct": Decimal("2.86"),
        "name": "Apple Inc.",
    }

    with patch("app.routers.holdings.get_stock_price", return_value=mock_stock_data):
        client.post("/holdings", json={"symbol": "AAPL", "shares": 10, "avg_cost": 150.00})
        client.post("/holdings", json={"symbol": "GOOGL", "shares": 5, "avg_cost": 2800.00})

    response = client.get("/holdings")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    symbols = {h["symbol"] for h in data}
    assert symbols == {"AAPL", "GOOGL"}


def test_update_holding(client, test_user):
    """Test updating a holding."""
    mock_stock_data = {
        "current_price": Decimal("180.00"),
        "previous_close": Decimal("175.00"),
        "daily_change_pct": Decimal("2.86"),
        "name": "Apple Inc.",
    }

    # Create holding
    with patch("app.routers.holdings.get_stock_price", return_value=mock_stock_data):
        create_response = client.post(
            "/holdings", json={"symbol": "AAPL", "shares": 10, "avg_cost": 150.00}
        )
    holding_id = create_response.json()["id"]

    # Update holding
    response = client.put(f"/holdings/{holding_id}", json={"shares": 20, "avg_cost": 160.00})

    assert response.status_code == 200
    data = response.json()
    assert Decimal(str(data["shares"])) == Decimal("20.00")
    assert Decimal(str(data["avg_cost"])) == Decimal("160.00")


def test_update_holding_partial(client, test_user):
    """Test partial update (only shares)."""
    mock_stock_data = {
        "current_price": Decimal("180.00"),
        "previous_close": Decimal("175.00"),
        "daily_change_pct": Decimal("2.86"),
        "name": "Apple Inc.",
    }

    with patch("app.routers.holdings.get_stock_price", return_value=mock_stock_data):
        create_response = client.post(
            "/holdings", json={"symbol": "AAPL", "shares": 10, "avg_cost": 150.00}
        )
    holding_id = create_response.json()["id"]

    # Update only shares
    response = client.put(f"/holdings/{holding_id}", json={"shares": 15})

    assert response.status_code == 200
    data = response.json()
    assert Decimal(str(data["shares"])) == Decimal("15.00")
    assert Decimal(str(data["avg_cost"])) == Decimal("150.00")  # Unchanged


def test_update_holding_not_found(client, test_user):
    """Test updating non-existent holding."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.put(f"/holdings/{fake_id}", json={"shares": 20})

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_delete_holding(client, test_user):
    """Test deleting a holding."""
    mock_stock_data = {
        "current_price": Decimal("180.00"),
        "previous_close": Decimal("175.00"),
        "daily_change_pct": Decimal("2.86"),
        "name": "Apple Inc.",
    }

    with patch("app.routers.holdings.get_stock_price", return_value=mock_stock_data):
        create_response = client.post(
            "/holdings", json={"symbol": "AAPL", "shares": 10, "avg_cost": 150.00}
        )
    holding_id = create_response.json()["id"]

    # Delete holding
    response = client.delete(f"/holdings/{holding_id}")
    assert response.status_code == 204

    # Verify it's gone
    list_response = client.get("/holdings")
    assert len(list_response.json()) == 0


def test_delete_holding_not_found(client, test_user):
    """Test deleting non-existent holding."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/holdings/{fake_id}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
