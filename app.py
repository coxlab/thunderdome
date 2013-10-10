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
    return render_template('gui.html', blah="open the bomb bay doors!")


@app.route('/open2')
def open2():
    return render_template('gui.html', blah="blah")

global a
a = 4

@app.route('/thenumber')
def thenumber():
    global a
    a += 500
    return str(a)


# -------------------------------------------------------
# Debug
# -------------------------------------------------------

if __name__ == "__main__":
    app.run(port=2665, debug=True)
