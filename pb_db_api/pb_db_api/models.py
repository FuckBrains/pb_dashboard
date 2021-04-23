"""DataBase models."""
from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class DesignMarket(Base):
    """Design market."""

    __tablename__ = 'design_markets'

    id = Column(Integer, primary_key=True)

    name = Column(Text(255), unique=True)
    balances = relationship('DesignMarketBalance', back_populates='design_market')


class DesignMarketBalance(Base):
    """Balance in design markets."""

    __tablename__ = 'design_markets_balance'

    id = Column(Integer, primary_key=True)

    id_design_market = Column(
        Integer, ForeignKey('design_markets.id'), nullable=False,
    )
    design_market = relationship('DesignMarket', back_populates='balances')

    balance = Column(Integer)
    create_at = Column(DateTime, default=datetime.datetime.utcnow)
