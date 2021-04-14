from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ
from flask import render_template

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    environ.get('SITE_LOGIN'): generate_password_hash(environ.get('SITE_PASS')),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def hello():

    return render_template('index.html', power_bi_url=environ.get('POWER_BI_URL'))