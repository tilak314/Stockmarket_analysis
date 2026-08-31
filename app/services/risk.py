def calculate_risk_level(
    price,
    sma_50,
    sma_200,
    rsi,
    debt_to_equity
):
    risk_score = 0

    # Technical risk
    if sma_200 is not None and price < sma_200:
        risk_score += 2
    elif sma_50 is not None and price < sma_50:
        risk_score += 1

    # RSI
    if rsi is not None and rsi < 30:
        risk_score += 1
    elif rsi is not None and rsi > 70:
        risk_score += 1

    # Debt
    if debt_to_equity is not None:
        if debt_to_equity > 100:
            risk_score += 2
        elif debt_to_equity > 50:
            risk_score += 1

    if risk_score >= 4:
        return "HIGH"
    elif risk_score >= 2:
        return "MEDIUM"
    else:
        return "LOW"


def calculate_stop_loss(price, sma_50, sma_200):

    supports = [
        x for x in [sma_50, sma_200]
        if x is not None and x < price
    ]

    if not supports:
        return None

    support = max(supports)

    stop_loss = support * 0.97

    return round(stop_loss, 2)