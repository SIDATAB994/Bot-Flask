from flask import Flask, jsonify
from strategy import get_daily_bets
import os

app = Flask(__name__)
bets_memory = []

@app.route("/")
def home():
    return "Bot actif"

@app.route("/run")
def run():
    global bets_memory
    bets_memory = get_daily_bets()
    return jsonify(bets_memory)

@app.route("/bets")
def bets():
    return jsonify(bets_memory)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
