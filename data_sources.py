import random

def fake_team_form():
    return round(random.uniform(0.4, 0.9), 2)

def enrich_with_stats(bet):
    form_home = fake_team_form()
    form_away = fake_team_form()

    # Ajustement probabilité
    adjusted_prob = bet["prob"] * (0.6 + 0.4 * form_home)

    bet["form_home"] = form_home
    bet["form_away"] = form_away
    bet["adjusted_prob"] = round(min(adjusted_prob, 0.95), 2)

    return bet
