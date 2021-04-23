from pb_db_api.db_utils import get_db
from pb_db_api.services import market
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pb_db_api.schemas import Command

router = APIRouter()


@router.post('/get')
def get(req_body: Command, db: Session = Depends(get_db)):
    """Get market names."""
    try:
        markets = market.get(db, req_body)
    except ValueError as val_err:
        return {'error': val_err.args}
    return markets
