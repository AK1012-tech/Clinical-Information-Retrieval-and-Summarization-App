from datetime import datetime

# Simple heuristic scoring for beginner use.
# You can extend this with more robust sources (e.g., SJR, Impact Factor APIs).

TOP_TIER = {
    "The Lancet", "Nature", "Science", "BMJ", "JAMA", "New England Journal of Medicine",
    "NEJM", "Annals of Internal Medicine", "Lancet"
}

def score_paper(paper: dict):
    score = 50
    journal = (paper.get("journal") or "").strip()

    # Journal prestige
    if any(j in journal for j in TOP_TIER):
        score += 30
    elif journal:
        score += 10

    # Recency bonus
    pub = paper.get("pubdate","")
    year = None
    for token in pub.split():
        if token.isdigit() and len(token) == 4:
            year = int(token)
            break
    if year:
        y_now = datetime.utcnow().year
        if y_now - year <= 2:
            score += 15
        elif y_now - year <= 5:
            score += 5

    # Bound score
    score = max(0, min(100, score))

    label = "High" if score >= 75 else "Medium" if score >= 55 else "Low"
    return {"score": score, "label": label}
