from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr


# User schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Holding schemas
class HoldingBase(BaseModel):
    symbol: str
    shares: Decimal
    avg_cost: Decimal


class HoldingCreate(HoldingBase):
    pass


class HoldingUpdate(BaseModel):
    shares: Decimal | None = None
    avg_cost: Decimal | None = None


class Holding(HoldingBase):
    id: UUID
    user_id: UUID
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Dashboard schemas
class DashboardHolding(BaseModel):
    symbol: str
    shares: Decimal
    avg_cost: Decimal
    current_price: Decimal
    previous_close: Decimal
    daily_change_pct: Decimal
    market_value: Decimal
    pnl: Decimal
    pnl_pct: Decimal
    allocation_pct: Decimal


class Dashboard(BaseModel):
    total_value: Decimal
    total_cost: Decimal
    total_pnl: Decimal
    total_pnl_pct: Decimal
    last_updated: datetime
    holdings: list[DashboardHolding]
