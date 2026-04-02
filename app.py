from flask import Flask, jsonify
from strategy import get_daily_bets
import os, datetime

app = Flask(__name__)

bets_memory = {}
bets_date = None

@app.route("/")
def home():
    return "Bot actif"

@app.route("/run")
def run():
    global bets_memory, bets_date
    bets_memory = get_daily_bets()
    bets_date = datetime.date.today()
    return jsonify(bets_memory)

@app.route("/bets")
def bets():
    global bets_memory, bets_date
    today = datetime.date.today()
    if bets_date != today or not bets_memory:
        bets_memory = get_daily_bets()
        bets_date = today
    return jsonify(bets_memory)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
