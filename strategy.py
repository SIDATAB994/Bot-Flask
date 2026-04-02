import requests
import os
import datetime

API_KEY = os.environ.get("e3848ed3063c719336b32e0b4861c7d9")  # Mettre dans Railway Environment

SPORTS = ["soccer_epl", "basketball_nba", "tennis_atp"]

def get_bets_for_date(target_date=None):
    """Récupère les paris pour une date donnée"""
    today = datetime.date.today() if not target_date else target_date
    bets = []

    if not API_KEY:
        return {"date": str(today),
                "simple": {"match": "Erreur API", "prediction": "-", "prob": 0, "odd": 0, "value": 0},
                "combo": []}

    try:
        for sport in SPORTS:
            url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals&dateFormat=iso"
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                continue
            events = response.json()
            for e in events[:5]:
                match = f"{e['home_team']} vs {e['away_team']}"
                bookmaker = e['bookmakers'][0]
                for market in bookmaker['markets']:
                    for outcome in market['outcomes']:
                        bets.append({
                            "match": match,
                            "sport": sport,
                            "type": market['key'],
                            "prediction": outcome['name'],
                            "odd": outcome['price'],
                            "prob": round(1/outcome['price'],2)
                        })

        # Calcul valeur
        for b in bets:
            b["value"] = round(b["prob"] * b["odd"],2)

        simple = max(bets, key=lambda x: x["prob"]) if bets else {"match":"Pas de données","prediction":"-","prob":0,"odd":0,"value":0}
        combo = sorted(bets, key=lambda x: x["value"], reverse=True)[:3]

        return {"date": str(today), "simple": simple, "combo": combo}

    except Exception as e:
        return {"date": str(today),
                "simple": {"match": f"Erreur: {str(e)}", "prediction":"-", "prob":0,"odd":0,"value":0},
                "combo": []}
