import requests
import os
import datetime
from analysis import value_score, confidence
from data_sources import enrich_with_stats

API_KEY = os.environ.get("API_KEY")

SPORTS = [
    "soccer_epl",
    "soccer_france_ligue_one",
    "basketball_nba"
]

def get_bets_for_date(target_date=None):

    today = datetime.date.today() if not target_date else target_date
    bets = []

    if not API_KEY:
        return {"error": "API_KEY manquante"}

    try:
        for sport in SPORTS:

            url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"
            res = requests.get(url, timeout=10)

            if res.status_code != 200:
                continue

            events = res.json()

            for e in events[:5]:

                match = f"{e['home_team']} vs {e['away_team']}"
                bookmaker = e['bookmakers'][0]

                for market in bookmaker['markets']:

                    for outcome in market['outcomes']:

                        odd = outcome['price']
                        prob = round(1 / odd, 2)

                        bet = {
                            "match": match,
                            "sport": sport,
                            "type": market['key'],
                            "prediction": outcome['name'],
                            "odd": odd,
                            "prob": prob
                        }

                        # 🔥 enrichissement stats
                        bet = enrich_with_stats(bet)

                        bet["value"] = value_score(bet["adjusted_prob"], odd)
                        bet["confidence"] = confidence(bet["adjusted_prob"], odd)

                        bets.append(bet)

        # 🔥 TRI ULTRA IMPORTANT
        bets = sorted(bets, key=lambda x: x["confidence"], reverse=True)

        # 🔥 FILTRE QUALITÉ
        bets = [b for b in bets if b["confidence"] > 2]

        simple = bets[0] if bets else {}
        combo = bets[:3]

        return {
            "date": str(today),
            "simple": simple,
            "combo": combo
        }

    except Exception as e:
        return {"error": str(e)}
