from os import environ

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

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
    return render_template('index.html')
