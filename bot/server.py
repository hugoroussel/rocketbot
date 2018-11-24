import json
from flask import Flask
from flask_cors import CORS
from Rocket import *

app = Flask(__name__)
CORS(app)

@app.route("/transactions")
def transactions():
    return json.dumps(Rocket.transactions())
    
@app.route("/test")
def test():
    Rocket.buy(1)
    Rocket.sell(1)
    return ''

@app.route("/buy/<value>")
def buy(value):
    Rocket.buy(value)
    return ''
    
@app.route("/sell/<value>")
def sell(value):
    Rocket.sell(value)
    return ''