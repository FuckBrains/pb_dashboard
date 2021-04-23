"""Pydantic's models."""

from typing import Optional
from datetime import datetime

from pydantic import BaseModel

from typing import List


class Command(BaseModel):

    cmd: str = 'all'


class Market(BaseModel):
    """Market balance model."""
    name: str


class Markets(BaseModel):
    """Market balance model."""
    names: List[Market]


class MarketBalanceGet(Market):

    start: Optional[datetime]
    end: Optional[datetime]


class MarketBalanceData(BaseModel):

    balance: int
    create_at: datetime


class MarketBalanceOut(Market):

    balances: List[MarketBalanceData]


class MarketBalanceList(BaseModel):
    markets: List[MarketBalanceOut] = []