"""Holdings CRUD API endpoints."""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.services.stock_service import StockNotFoundError, get_stock_price

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/holdings", tags=["holdings"])


def _ensure_user_exists(db: Session, user_id: UUID, email: str | None = None) -> None:
    """Create user record if it doesn't exist yet."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        user = models.User(id=user_id, email=email or "")
        db.add(user)
        db.commit()


@router.get("", response_model=list[schemas.Holding])
def list_holdings(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Get all holdings for the current user.

    Returns:
        List of holdings with details
    """
    user_id = UUID(current_user["sub"])
    _ensure_user_exists(db, user_id, current_user.get("email"))
    holdings = db.query(models.Holding).filter(models.Holding.user_id == user_id).all()
    return holdings


@router.post("", response_model=schemas.Holding, status_code=status.HTTP_201_CREATED)
def create_or_update_holding(
    holding_data: schemas.HoldingCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new holding or update existing one with weighted average.

    If a holding with the same symbol exists, it will calculate weighted average:
    - new_shares = existing_shares + incoming_shares
    - new_avg_cost = (existing_shares * existing_avg_cost + incoming_shares * incoming_avg_cost) / new_shares

    Args:
        holding_data: Holding creation data (symbol, shares, avg_cost)

    Returns:
        Created or updated holding

    Raises:
        HTTPException 400: If stock symbol is invalid
        HTTPException 500: If stock API fails
    """
    user_id = UUID(current_user["sub"])
    _ensure_user_exists(db, user_id, current_user.get("email"))

    # Fetch stock name from yfinance
    try:
        stock_data = get_stock_price(holding_data.symbol.upper())
        stock_name = stock_data["name"]
    except StockNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid stock symbol: {holding_data.symbol}",
        ) from e
    except Exception as e:
        logger.error(f"Failed to fetch stock data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch stock information",
        ) from e

    # Check if holding already exists for this user and symbol
    existing_holding = (
        db.query(models.Holding)
        .filter(
            models.Holding.user_id == user_id,
            models.Holding.symbol == holding_data.symbol.upper(),
        )
        .first()
    )

    if existing_holding:
        # Calculate weighted average
        old_shares = existing_holding.shares
        old_avg_cost = existing_holding.avg_cost
        new_shares_input = holding_data.shares
        new_avg_cost_input = holding_data.avg_cost

        # New total shares
        total_shares = old_shares + new_shares_input

        # Weighted average cost
        weighted_avg_cost = (
            (old_shares * old_avg_cost) + (new_shares_input * new_avg_cost_input)
        ) / total_shares

        # Update existing holding
        existing_holding.shares = total_shares
        existing_holding.avg_cost = weighted_avg_cost

        db.commit()
        db.refresh(existing_holding)

        logger.info(
            f"Updated holding {holding_data.symbol}: {old_shares} + {new_shares_input} = {total_shares} shares, "
            f"avg_cost ${old_avg_cost} -> ${weighted_avg_cost}"
        )

        return existing_holding
    else:
        # Create new holding
        new_holding = models.Holding(
            user_id=user_id,
            symbol=holding_data.symbol.upper(),
            name=stock_name,
            shares=holding_data.shares,
            avg_cost=holding_data.avg_cost,
        )

        db.add(new_holding)
        db.commit()
        db.refresh(new_holding)

        logger.info(f"Created new holding: {holding_data.symbol} - {holding_data.shares} shares")

        return new_holding


@router.put("/{holding_id}", response_model=schemas.Holding)
def update_holding(
    holding_id: UUID,
    holding_update: schemas.HoldingUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update a holding's shares or average cost.

    Args:
        holding_id: Holding UUID
        holding_update: Update data (shares and/or avg_cost)

    Returns:
        Updated holding

    Raises:
        HTTPException 404: If holding not found
    """
    user_id = UUID(current_user["sub"])
    holding = (
        db.query(models.Holding)
        .filter(
            models.Holding.id == holding_id,
            models.Holding.user_id == user_id,
        )
        .first()
    )

    if not holding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Holding with id {holding_id} not found",
        )

    # Update only provided fields
    if holding_update.shares is not None:
        holding.shares = holding_update.shares

    if holding_update.avg_cost is not None:
        holding.avg_cost = holding_update.avg_cost

    db.commit()
    db.refresh(holding)

    logger.info(
        f"Updated holding {holding_id}: shares={holding.shares}, avg_cost={holding.avg_cost}"
    )

    return holding


@router.delete("/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_holding(
    holding_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a holding.

    Args:
        holding_id: Holding UUID

    Raises:
        HTTPException 404: If holding not found
    """
    user_id = UUID(current_user["sub"])
    holding = (
        db.query(models.Holding)
        .filter(
            models.Holding.id == holding_id,
            models.Holding.user_id == user_id,
        )
        .first()
    )

    if not holding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Holding with id {holding_id} not found",
        )

    db.delete(holding)
    db.commit()

    logger.info(f"Deleted holding {holding_id}: {holding.symbol}")

    return None
