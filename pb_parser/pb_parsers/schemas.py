"""Pydantic's models."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Market(BaseModel):
    """Market balance model."""
    name: str
    display_name: Optional[str]


class MarketBalanceMake(Market):

    balance: int


class MarketBalanceGet(Market):

    start: Optional[datetime]
    end: Optional[datetime]


class MarketBalanceData(BaseModel):

    balance: int
    create_at: datetime


class MarketBalanceOut(Market):

    balances: List[MarketBalanceData]
