from clickhouse_driver.client import Client
from os import environ
import requests
import schemas

client = Client(
    host=environ.get('CH_HOST'),
    database=environ.get('CH_DB'),
    user=environ.get('CH_USER'),
    password=environ.get('CH_PASS')
)
DB_API_ENDPOINT = environ.get('DB_API_ENDPOINT') or 'http://127.0.0.1:8000/{}/{}'


def get_subs_in_use(period='month'):
    q_period = 'month' if period == 'month' else 'year'
    resp = client.execute(
        """
        SELECT COUNT(*) FROM (
        SELECT * FROM subscriptions WHERE end_date>NOW()) AS subs JOIN (
        SELECT * FROM orders WHERE payed=1 AND orderable_type LIKE '%Subscription') AS ord
        ON ord.user_id=subs.user_id
        WHERE ord.period='{period}'
        """.format(
            period=q_period
        )
    )
    return resp[0][0]


def get_subs_active(period='month'):
    q_period = 'month' if period == 'month' else 'year'
    resp = client.execute(
        """
        SELECT COUNT(*) FROM (
        SELECT * FROM subscriptions WHERE status='active') AS subs JOIN (
        SELECT * FROM orders WHERE payed=1 AND orderable_type LIKE '%Subscription') AS ord
        ON ord.user_id=subs.user_id
        WHERE ord.period='{period}'
        """.format(
            period=q_period
        )
    )
    return resp[0][0]


def get_subs_all(period='month'):
    q_period = 'month' if period == 'month' else 'year'
    resp = client.execute(
        """SELECT COUNT(*) FROM orders
        WHERE period='{period}' AND payed=1
        """.format(period=q_period)
    )
    return resp[0][0]


def get_subs_graph():
    resp = client.execute(
        """
        SELECT SUM(price), toMonth(created_at), toYear(created_at) FROM orders
        WHERE period IS NOT null AND payed=1 AND currency='usd'
        GROUP BY toMonth(created_at), toYear(created_at) ORDER BY
        toYear(created_at), toMonth(created_at)
        """
    )
    graph = {'x': [], 'y': [], 'type': 'scatter', 'name': 'Income'}

    for month_data in resp:
        income, month, year = month_data
        graph['y'].append(income)
        graph['x'].append('{}-{}'.format(year, month))
    return [graph]


def get_market_last_balances():
    req_data = schemas.Command(
        cmd='all'
    )
    markets = schemas.Markets.parse_raw(
        requests.post(DB_API_ENDPOINT.format('market', 'get'), req_data.json()).text
    )
    market_balances = schemas.MarketBalanceList()
    print(markets)
    for market in markets.names:
        req_data = schemas.MarketBalanceGet(
            name=market.name
        )
        market_balances.markets.append(
            schemas.MarketBalanceOut.parse_raw(
                requests.post(
                    DB_API_ENDPOINT.format('balance', 'get'), req_data.json()
                ).text
            )
        )
    print(market_balances)
    return market_balances
