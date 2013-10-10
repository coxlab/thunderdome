#!/usr/bin/env python

from flask import (Flask,
                   g,
                   request,
                   render_template,
                   redirect,
                   url_for,
                   jsonify,
                   abort)


# -------------------------------------------------------
# Flask App Setup (flask + flask-restful)
# -------------------------------------------------------

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('gui.html')

@app.route('/open1')
def open1():
    return "open the bomb bay doors!"



# -------------------------------------------------------
# Debug
# -------------------------------------------------------

if __name__ == "__main__":
    app.run(port=2665, debug=True)
