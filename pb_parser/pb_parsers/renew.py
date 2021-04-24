from pb_parsers import schemas, parsers
from os import environ
import requests
from selenium import webdriver

DB_API_ENDPOINT = environ.get('DB_API_ENDPOINT') or 'http://127.0.0.1:8000/{}/{}'

CREATIVE_MARKET_NAME = 'creativemarket.com'
CREATIVE_MARKET_DISPLAY_NAME = 'creativemarket.com - PB'
CREATIVE_MARKET_USERNAME = environ.get('CREATIVE_MARKET_USERNAME') or ''
CREATIVE_MARKET_PASSWORD = environ.get('CREATIVE_MARKET_PASSWORD') or ''

CREATIVE_MARKET_SQUAD_NAME = 'creativemarket.com - DesignSquad'
CREATIVE_MARKET_SQUAD_DISPLAY_NAME = 'creativemarket.com - DS'
CREATIVE_MARKET_SQUAD_USERNAME = environ.get('CREATIVE_MARKET_SQUAD_USERNAME') or ''
CREATIVE_MARKET_SQUAD_PASSWORD = environ.get('CREATIVE_MARKET_SQUAD_PASSWORD') or ''

ELEMENTS_NAME = 'elements.envato.com'
ELEMENTS_DISPLAY_NAME = 'elements.envato.com'
ELEMENTS_USERNAME = environ.get('ELEMENTS_USERNAME') or ''
ELEMENTS_PASSWORD = environ.get('ELEMENTS_PASSWORD') or ''

FREEPIK_NAME = 'freepik.com'
FREEPIK_DISPLAY_NAME = 'freepik.com'
FREEPIK_USERNAME = environ.get('FREEPIK_USERNAME') or ''
FREEPIK_PASSWORD = environ.get('FREEPIK_PASSWORD') or ''


def creative_balance(driver: webdriver.Remote):
    out_schema = schemas.MarketBalanceMake(
        name=CREATIVE_MARKET_NAME,
        display_name=CREATIVE_MARKET_DISPLAY_NAME,
        balance=parsers.get_creative_ballance(
            driver, CREATIVE_MARKET_USERNAME, CREATIVE_MARKET_PASSWORD
        )
    )
    requests.post(DB_API_ENDPOINT.format('balance', 'make'), out_schema.json())
    out_schema = schemas.MarketBalanceMake(
        name=CREATIVE_MARKET_SQUAD_NAME,
        display_name=CREATIVE_MARKET_SQUAD_DISPLAY_NAME,
        balance=parsers.get_creative_ballance(
            driver, CREATIVE_MARKET_SQUAD_USERNAME, CREATIVE_MARKET_SQUAD_PASSWORD
        )
    )
    requests.post(DB_API_ENDPOINT.format('balance', 'make'), out_schema.json())


def elements_balance(driver: webdriver.Remote):
    out_schema = schemas.MarketBalanceMake(
        name=ELEMENTS_NAME,
        display_name=ELEMENTS_DISPLAY_NAME,
        balance=parsers.get_elements_ballance(driver, ELEMENTS_USERNAME, ELEMENTS_PASSWORD)
    )
    requests.post(DB_API_ENDPOINT.format('balance', 'make'), out_schema.json())


def freepik_balance(driver: webdriver.Remote, eurusd: float):
    out_schema = schemas.MarketBalanceMake(
        name=FREEPIK_NAME,
        display_name=FREEPIK_DISPLAY_NAME,
        balance=int(
            eurusd * parsers.get_freepik_ballance(driver, FREEPIK_USERNAME, FREEPIK_PASSWORD)
        )
    )
    requests.post(DB_API_ENDPOINT.format('balance', 'make'), out_schema.json())
