import requests
import datetime

API_KEY = "e3848ed3063c719336b32e0b4861c7d9"  # à créer sur theoddsapi.com
SPORTS = ["soccer_epl", "basketball_nba", "tennis_atp"]

def get_daily_bets():
    today = datetime.date.today()
    bets = []

    for sport in SPORTS:
        url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,spreads,totals&dateFormat=iso"
        response = requests.get(url)
        if response.status_code == 200:
            events = response.json()
            for e in events:
                match = f"{e['home_team']} vs {e['away_team']}"
                # Exemple simple : prendre le premier bookmaker
                bookmaker = e['bookmakers'][0]
                for market in bookmaker['markets']:
                    for outcome in market['outcomes']:
                        bets.append({
                            "match": match,
                            "sport": sport,
                            "type": market['key'],      # h2h / spreads / totals
                            "prediction": outcome['name'],
                            "odd": outcome['price'],
                            "prob": round(1/outcome['price'], 2)  # approximation
                        })

    # Calcul valeur = prob * odd
    for b in bets:
        b["value"] = round(b["prob"] * b["odd"], 2)

    # Simple et combo
    simple = max(bets, key=lambda x: x["prob"])
    combo = sorted(bets, key=lambda x: x["value"], reverse=True)[:3]

    return {
        "date": str(today),
        "simple": simple,
        "combo": combo
    }
