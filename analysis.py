def implied_prob(odd):
    return 1 / odd

def value_score(prob, odd):
    return round(prob * odd, 2)

def edge(prob, odd):
    return round(prob - implied_prob(odd), 3)

def confidence(prob, odd):
    e = edge(prob, odd)
    return round(max(0, e * 100), 2)
