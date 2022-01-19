from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = 'joflsadfsywj3k34hxvdsa0fjlajdfljdsjl'

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='bc9VXejShx5SNXHgw6C8vEjAe0NDIdS0',
    client_secret='AjVILJrIhfqfMz2-k_ptfNBiNYz-sAtGkmvwYZo0i-gPoOVvjP7sndD5T-lHp-Ko',
    api_base_url='https://codememory.jp.auth0.com',
    access_token_url='https://codememory.jp.auth0.com/oauth/token',
    authorize_url='https://codememory.jp.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

app.debug =  True
app.run()