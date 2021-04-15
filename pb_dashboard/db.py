from clickhouse_driver.client import Client
from os import environ

client = Client(
    host=environ.get('CH_HOST'),
    database=environ.get('CH_DB'),
    user=environ.get('CH_USER'),
    password=environ.get('CH_PASS')
)


def get_subs_in_use(period='month', ago=0):
    q_period = 'month' if period == 'month' else 'year'
    resp = client.execute(
        """SELECT COUNT(*) FROM orders
        WHERE period='{period}' AND payed=1 AND updated_at > (NOW() - INTERVAL {ago} {period})
        """.format(
            period=q_period,
            ago=1 + ago,
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
        SELECT COUNT(*), toMonth(created_at), toYear(created_at) FROM orders
        WHERE period IS NOT null AND payed=1
        GROUP BY toMonth(created_at), toYear(created_at) ORDER BY
        toYear(created_at), toMonth(created_at)
        """
    )
    num_new_subs = []
    date = []
    for month_data in resp:
        _num_new_subs, month, year = month_data
        num_new_subs.append(_num_new_subs)
        date.append('{}-{}'.format(year, month))
    return num_new_subs, date
