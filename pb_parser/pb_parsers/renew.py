from pb_parsers import schemas, parsers
from os import environ
import requests

DB_API_ENDPOINT = environ.get('DB_API_ENDPOINT') or 'http://127.0.0.1:8000/{}/{}'

CREATIVE_MARKET_NAME = 'creativemarket.com'
CREATIVE_MARKET_USERNAME = environ.get('CREATIVE_MARKET_USERNAME')
CREATIVE_MARKET_PASSWORD = environ.get('CREATIVE_MARKET_PASSWORD')


def creative_balance():
    out_schema = schemas.MarketBalanceMake(
        name=CREATIVE_MARKET_NAME,
        balance=parsers.get_creative_ballance(CREATIVE_MARKET_USERNAME, CREATIVE_MARKET_PASSWORD)
    )
    print(out_schema.json())
    print(DB_API_ENDPOINT.format('balance', 'make'))
    requests.post(DB_API_ENDPOINT.format('balance', 'make'), out_schema.json())