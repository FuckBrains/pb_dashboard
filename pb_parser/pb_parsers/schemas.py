"""Pydantic's models."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MarketBalanceBase(BaseModel):
    """Market balance model."""
    name: str


class MarketBalanceMake(MarketBalanceBase):

    balance: int


class MarketBalanceGet(MarketBalanceBase):

    start: Optional[datetime]
    end: Optional[datetime]


class MarketBalanceData(BaseModel):

    balance: int
    create_at: datetime


class MarketBalanceOut(MarketBalanceBase):

    balances: List[MarketBalanceData]
