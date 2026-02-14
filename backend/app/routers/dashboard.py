"""Dashboard API endpoint."""

import logging
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.routers.holdings import HARDCODED_USER_ID
from app.services.stock_service import get_multiple_prices

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=schemas.Dashboard)
def get_dashboard(db: Session = Depends(get_db)):
    """
    Get portfolio dashboard with real-time stock prices and calculations.

    Returns:
        Dashboard data including:
        - Total portfolio value, cost, P&L
        - Individual holdings with current prices
        - Daily change percentages
        - Allocation percentages

    Raises:
        HTTPException 404: If no holdings found
    """
    # Fetch all holdings for user
    holdings = db.query(models.Holding).filter(models.Holding.user_id == HARDCODED_USER_ID).all()

    if not holdings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No holdings found for user",
        )

    # Extract symbols
    symbols = [holding.symbol for holding in holdings]

    # Fetch current prices for all symbols
    logger.info(f"Fetching prices for {len(symbols)} symbols: {symbols}")
    price_data = get_multiple_prices(symbols)

    # Calculate metrics for each holding
    dashboard_holdings = []
    total_value = Decimal(0)
    total_cost = Decimal(0)

    for holding in holdings:
        stock_prices = price_data.get(holding.symbol)

        # Skip holdings where price fetch failed
        if stock_prices is None:
            logger.warning(f"Skipping {holding.symbol} - price data unavailable")
            continue

        current_price = stock_prices["current_price"]
        previous_close = stock_prices["previous_close"]
        daily_change_pct = stock_prices["daily_change_pct"]

        # Calculate holding metrics
        market_value = holding.shares * current_price
        cost_basis = holding.shares * holding.avg_cost
        pnl = market_value - cost_basis

        if cost_basis > 0:
            pnl_pct = (pnl / cost_basis) * 100
        else:
            pnl_pct = Decimal(0)

        # Accumulate totals
        total_value += market_value
        total_cost += cost_basis

        dashboard_holdings.append(
            schemas.DashboardHolding(
                symbol=holding.symbol,
                shares=holding.shares,
                avg_cost=holding.avg_cost,
                current_price=current_price,
                previous_close=previous_close,
                daily_change_pct=daily_change_pct,
                market_value=market_value,
                pnl=pnl,
                pnl_pct=pnl_pct,
                allocation_pct=Decimal(0),  # Will calculate after total_value is known
            )
        )

    # Handle case where all price fetches failed
    if not dashboard_holdings:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to fetch stock prices for any holdings",
        )

    # Calculate portfolio totals
    total_pnl = total_value - total_cost

    if total_cost > 0:
        total_pnl_pct = (total_pnl / total_cost) * 100
    else:
        total_pnl_pct = Decimal(0)

    # Calculate allocation percentages
    for holding_data in dashboard_holdings:
        if total_value > 0:
            holding_data.allocation_pct = (holding_data.market_value / total_value) * 100
        else:
            holding_data.allocation_pct = Decimal(0)

    logger.info(
        f"Dashboard calculated: {len(dashboard_holdings)} holdings, "
        f"total_value=${total_value}, total_pnl=${total_pnl} ({total_pnl_pct:.2f}%)"
    )

    return schemas.Dashboard(
        total_value=total_value,
        total_cost=total_cost,
        total_pnl=total_pnl,
        total_pnl_pct=total_pnl_pct,
        last_updated=datetime.now(),
        holdings=dashboard_holdings,
    )
