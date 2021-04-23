"""Data base app."""
from pb_db_api.db_utils import get_db
from pb_db_api.schemas import MarketBalanceGet, MarketBalanceMake
from pb_db_api.services import balance
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/make')
def make(req_body: MarketBalanceMake, db: Session = Depends(get_db)):
    """Make new balance."""
    try:
        _balance = balance.make(db, req_body)
    except ValueError as val_err:
        return {'error': val_err.args}
    return _balance


@router.post('/get')
def get(req_body: MarketBalanceGet, db: Session = Depends(get_db)):
    """Make and return new chapter."""
    try:
        _balances = balance.get(db, req_body)
    except ValueError as val_err:
        return {'error': val_err.args}
    return _balances
