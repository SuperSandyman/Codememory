from flask import Blueprint

static = Blueprint("static", __name__, static_url_path='/static', static_folder='./static')
img = Blueprint("img", __name__, static_url_path='/img', static_folder='./assets/img')