from flask import Flask, jsonify, request
from strategy import get_bets_for_date
import datetime, os

app = Flask(__name__)

@app.route("/")
def home():
    return "Betting AI actif"

@app.route("/bets")
def bets():
    date_str = request.args.get("date")

    target_date = None
    if date_str:
        try:
            target_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            pass

    return jsonify(get_bets_for_date(target_date))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
