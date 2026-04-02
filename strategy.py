import random
import datetime

def get_daily_bets():
    """
    Analyse ultra poussée (simulation)
    - Compare tous les événements du jour (multi-sports)
    - Génère un combiné fiable
    """

    today = datetime.date.today()

    # Exemple simulé de données sportives
    events = [
        {"sport": "Football", "match": "PSG vs Lyon", "prob": 0.68, "odd": 1.55},
        {"sport": "Football", "match": "Inter vs Roma", "prob": 0.64, "odd": 1.60},
        {"sport": "Basketball", "match": "Lakers vs Warriors", "prob": 0.60, "odd": 1.75},
        {"sport": "Tennis", "match": "Djokovic vs Nadal", "prob": 0.62, "odd": 1.70},
        {"sport": "Hockey", "match": "Maple Leafs vs Canadiens", "prob": 0.65, "odd": 1.50},
    ]

    # Calcul ultra poussée : value = prob * odd, tri, combinés
    for e in events:
        e["value"] = round(e["prob"] * e["odd"], 2)

    # Simple : pari avec meilleure probabilité
    simple = max(events, key=lambda x: x["prob"])

    # Combo : top 2 ou top 3 selon valeur
    combo = sorted(events, key=lambda x: x["value"], reverse=True)[:3]

    # Ajouter la date
    result = {
        "date": str(today),
        "simple": simple,
        "combo": combo
    }

    return result
