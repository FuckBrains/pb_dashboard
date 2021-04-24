from pb_parsers import schemas, parsers
from os import environ
import requests
from time import sleep

DB_API_ENDPOINT = environ.get('DB_API_ENDPOINT') or 'http://127.0.0.1:8000/{}/{}'

CREATIVE_MARKET_NAME = 'creativemarket.com'
CREATIVE_MARKET_USERNAME = environ.get('CREATIVE_MARKET_USERNAME')
CREATIVE_MARKET_PASSWORD = environ.get('CREATIVE_MARKET_PASSWORD')

CREATIVE_MARKET_SQUAD_NAME = 'creativemarket.com - DesignSquad'
CREATIVE_MARKET_SQUAD_USERNAME = environ.get('CREATIVE_MARKET_SQUAD_USERNAME')
CREATIVE_MARKET_SQUAD_PASSWORD = environ.get('CREATIVE_MARKET_SQUAD_PASSWORD')

ELEMENTS_NAME = 'elements.envato.com'
ELEMENTS_USERNAME = environ.get('ELEMENTS_USERNAME')
ELEMENTS_PASSWORD = environ.get('ELEMENTS_PASSWORD')


def creative_balance():
    out_schema = schemas.MarketBalanceMake(
        name=CREATIVE_MARKET_NAME,
        balance=parsers.get_creative_ballance(CREATIVE_MARKET_USERNAME, CREATIVE_MARKET_PASSWORD)
    )
    requests.post(DB_API_ENDPOINT.format('balance', 'make'), out_schema.json())
    sleep(30)
    out_schema = schemas.MarketBalanceMake(
        name=CREATIVE_MARKET_SQUAD_NAME,
        balance=parsers.get_creative_ballance(
            CREATIVE_MARKET_SQUAD_USERNAME, CREATIVE_MARKET_SQUAD_PASSWORD
        )
    )
    requests.post(DB_API_ENDPOINT.format('balance', 'make'), out_schema.json())


def elements_balance():
    out_schema = schemas.MarketBalanceMake(
        name=ELEMENTS_NAME,
        balance=parsers.get_elements_ballance(ELEMENTS_USERNAME, ELEMENTS_PASSWORD)
    )
    requests.post(DB_API_ENDPOINT.format('balance', 'make'), out_schema.json())
