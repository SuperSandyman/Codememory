from distutils.log import debug
from flask import Flask, render_template, url_for
import urllib.request
import urllib.parse
import setBrueprint
import json
import flask_oauthlib.client
from jose import jwt
from jwt.algorithms import RSAAlgorithm

app = Flask(__name__, static_folder="assets")

app.register_blueprint(setBrueprint.static)
app.register_blueprint(setBrueprint.img)

AUTH0_CLIENT_ID = 'bc9VXejShx5SNXHgw6C8vEjAe0NDIdS0'
AUTH0_CLIENT_SECRET = 'AjVILJrIhfqfMz2-k_ptfNBiNYz-sAtGkmvwYZo0i-gPoOVvjP7sndD5T-lHp-Ko'
AUTH0_DOMAIN = 'codememory.jp.auth0.com'
app.secret_key = 'jfjar4oodljfoaurae4owuojdlf'

oauth = flask_oauthlib.client.OAuth(app)

auth0 = oauth.remote_app(
    'auth0',
    consumer_key=AUTH0_CLIENT_ID,
    consumer_secret=AUTH0_CLIENT_SECRET,
    request_token_params={
        'scope': 'openid profile',
        'audience': 'https://{}/userinfo'.format(AUTH0_DOMAIN),
    },
    base_url='https://{}'.format(AUTH0_DOMAIN),
    access_token_method='POST',
    access_token_url='/oauth/token',
    authorize_url='/authorize',
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return auth0.authorize(callback=url_for('auth_callback', _external=True))

@app.route('/callback')
def auth_callback():
    # Auth0がくれた情報を取得する。
    resp = auth0.authorized_response()
    if resp is None:
        return 'nothing data', 403

    # 署名をチェックするための情報を取得してくる。
    jwks = json.loads(urllib.request.urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json").read())

    # JWT形式のデータを復号して、ユーザーについての情報を得る。
    # ついでに、署名が正しいかどうか検証している。
    try:
        payload = jwt.decode(resp['id_token'], RSAAlgorithm.from_jwk( json.dumps(jwks['keys'][0])), audience=AUTH0_CLIENT_ID, algorithms='RS256')
    except Exception as e:
        print(e)
        return 'something wrong', 403  # 署名がおかしい。

    # flaskのSessionを使ってcookieにユーザーデータを保存。
    Flask.session['profile'] = {
        'id': payload['sub'],
        'name': payload['name'],
        'picture': payload['picture'],
    }

    # マイページに飛ばす。
    return Flask.redirect(url_for('mypage'))

@app.route('/mypage')
def mypage():
    if 'profile' not in Flask.session:
        return Flask.redirect(Flask.url_for('login'))

    return '''
        <img src="{picture}"><br>
        name: <b>{name}</b><br>
        ID: <b>{id}</b><br>
        <br>
        <a href="/">back to top</a>
    '''.format(**Flask.session['profile'])

@app.route('/logout')
def logout():
    del Flask.session['profile']

    params = {'returnTo': Flask.url_for('index', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return Flask.redirect(auth0.base_url + '/v2/logout?' + urllib.parse.urlencode(params))

if __name__ == '__main__':
    app.run(debug=True)