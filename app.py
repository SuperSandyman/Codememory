from distutils.log import debug
from flask import Flask, render_template
import setBrueprint

app = Flask(__name__, static_folder="assets")

app.register_blueprint(setBrueprint.static)
app.register_blueprint(setBrueprint.img)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)