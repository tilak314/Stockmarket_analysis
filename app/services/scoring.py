# . Technical score
def calculate_technical_score(
    price,
    sma_20,
    sma_50,
    sma_200,
    rsi
):
    score = 50

    # Price vs moving averages
    if sma_20:
        if price > sma_20:
            score += 10
        else:
            score -= 10

    if sma_50:
        if price > sma_50:
            score += 10
        else:
            score -= 10

    if sma_200:
        if price > sma_200:
            score += 15
        else:
            score -= 15

    # RSI
    if rsi:
        if 50 <= rsi <= 65:
            score += 10
        elif 65 < rsi <= 70:
            score += 5
        elif rsi > 70:
            score -= 10
        elif 30 <= rsi < 50:
            score -= 5
        elif rsi < 30:
            score += 2

    return max(0, min(100, score))




# 2. fundamental score
def calculate_fundamental_score(
    revenue_growth,
    profit_margin,
    roe,
    roa,
    debt_to_equity
):
    score = 50

    # Revenue growth
    if revenue_growth is not None:
        if revenue_growth > 0.20:
            score += 15
        elif revenue_growth > 0.10:
            score += 10
        elif revenue_growth > 0:
            score += 5
        else:
            score -= 10

    # Profit margin
    if profit_margin is not None:
        if profit_margin > 0.20:
            score += 15
        elif profit_margin > 0.10:
            score += 10
        elif profit_margin > 0:
            score += 5
        else:
            score -= 10

    # ROE
    if roe is not None:
        if roe > 0.20:
            score += 10
        elif roe > 0.10:
            score += 5
        elif roe < 0:
            score -= 5

    # ROA
    if roa is not None:
        if roa > 0.10:
            score += 5
        elif roa < 0:
            score -= 5

    # Debt to equity
    if debt_to_equity is not None:
        if debt_to_equity > 100:
            score -= 15
        elif debt_to_equity > 50:
            score -= 10
        elif debt_to_equity > 25:
            score -= 5

    return max(0, min(100, score))



# 3. news score
def calculate_news_score(news_data):
    if not news_data:
        return 50

    score = 50

    positive_words = [
        "growth", "profit", "partnership", "expansion",
        "approval", "launch", "order", "contract"
    ]

    negative_words = [
        "loss", "decline", "fall", "fraud", "debt",
        "downgrade", "lawsuit", "weak", "drop"
    ]

    for news in news_data:
        title = news.get("title", "").lower()

        if any(word in title for word in positive_words):
            score += 5

        if any(word in title for word in negative_words):
            score -= 5

    return max(0, min(100, score))



# 4. valuation score
def calculate_valuation_score(pe_ratio, forward_pe, revenue_growth):
    score = 50

    # P/E
    if pe_ratio is not None:
        if pe_ratio < 15:
            score += 20
        elif pe_ratio < 25:
            score += 10
        elif pe_ratio > 50:
            score -= 15
        elif pe_ratio > 35:
            score -= 10

    # Forward P/E
    if forward_pe is not None:
        if forward_pe < 15:
            score += 15
        elif forward_pe < 25:
            score += 10
        elif forward_pe > 50:
            score -= 15
        elif forward_pe > 35:
            score -= 10

    # Growth can justify higher valuation
    if revenue_growth is not None:
        if revenue_growth > 0.20:
            score += 10
        elif revenue_growth < 0:
            score -= 10

    return max(0, min(100, score))


# 5. market score
def calculate_market_score():
    # Basic placeholder for now
    # We will improve this later using NIFTY/SENSEX/sector data.
    return 50


# Final weighted score of above 5 scores
def calculate_final_stock_score(
    technical_score,
    fundamental_score,
    news_score,
    market_score,
    valuation_score
):
    final_score = (
        technical_score * 0.20 +
        fundamental_score * 0.30 +
        news_score * 0.15 +
        market_score * 0.15 +
        valuation_score * 0.20
    )

    return round(final_score)


def get_score_recommendation(final_stock_score):

    if final_stock_score >= 80:
        return "BUY"

    elif final_stock_score >= 65:
        return "ACCUMULATE"

    elif final_stock_score >= 50:
        return "HOLD"

    elif final_stock_score >= 35:
        return "AVOID"

    else:
        return "SELL"



def calculate_buy_zone(
    price,
    sma_20,
    sma_50,
    sma_200
):
    supports = [
        x for x in [sma_20, sma_50, sma_200]
        if x is not None
    ]

    if not supports:
        return None, None

    # Nearest support below current price
    below_price = [x for x in supports if x <= price]

    if not below_price:
        return None, None

    nearest_support = max(below_price)

    # Allow a small range around support
    buy_zone_min = nearest_support * 0.98
    buy_zone_max = nearest_support * 1.02

    return (
        round(buy_zone_min, 2),
        round(buy_zone_max, 2)
    )


def calculate_market_score(
    current_price,
    sma_50,
    sma_200,
    trend
):
    score = 50

    if trend == "BULLISH":
        score += 25
    elif trend == "BEARISH":
        score -= 25

    if current_price > sma_50:
        score += 10
    else:
        score -= 10

    if current_price > sma_200:
        score += 10
    else:
        score -= 10

    return max(0, min(100, score))