"""Routes."""
from fastapi import APIRouter

from pb_db_api.local_routes import balance, market

routes = APIRouter()

routes.include_router(balance.router, prefix='/balance')
routes.include_router(market.router, prefix='/market')
