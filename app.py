from flask import Flask, jsonify, request
from strategy import get_bets_for_date
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
    bets_memory = get_bets_for_date()
    bets_date = datetime.date.today()
    return jsonify(bets_memory)

@app.route("/bets")
def bets():
    global bets_memory, bets_date
    date_str = request.args.get("date")
    target_date = None
    if date_str:
        try:
            target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            target_date = None
    if bets_date != target_date or not bets_memory:
        bets_memory = get_bets_for_date(target_date)
        bets_date = target_date or datetime.date.today()
    return jsonify(bets_memory)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
