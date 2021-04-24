from os import environ

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

import db

app = Flask(__name__)
auth = HTTPBasicAuth()
bootstrap = Bootstrap(app)

users = {
    environ.get('SITE_LOGIN') or 'root': generate_password_hash(environ.get('SITE_PASS') or 'pass'),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/')
@auth.login_required
def index():
    return render_template('index.html')


@app.route('/trafic-data/')
@auth.login_required
def trafic_data():
    return render_template('trafic_data.html', power_bi_url=environ.get('POWER_BI_URL'))


@app.route('/subscription-data/')
@auth.login_required
def subscription_data():
    subs = [
        {
            'period': 'Month',
            'all': db.get_subs_all(),
            'in_use': db.get_subs_in_use(),
            'active': db.get_subs_active()
        },
        {
            'period': 'Year',
            'all': db.get_subs_all(period='year'),
            'in_use': db.get_subs_in_use(period='year'),
            'active': db.get_subs_active(period='year')
        },
    ]
    graph_data = db.get_subs_graph()

    return render_template('subscription_data.html', subs=subs, graph_data=graph_data)


@app.route('/accouns-data/')
@auth.login_required
def accounts_data():
    balances = db.get_market_last_balances()
    sum_of_money = 0
    for market in balances.markets:
        sum_of_money += market.balances[0].balance
    return render_template('accounts_data.html', balances=balances, sum_of_money=sum_of_money)
