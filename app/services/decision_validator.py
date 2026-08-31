def validate_decision(recommendation, price_action):

    rec = recommendation.recommendation

    if rec == "SELL":
        price_action["action"] = "SELL"
        price_action["holder_action"] = "SELL"
        price_action["new_investor_action"] = "AVOID"

    elif rec == "AVOID":
        price_action["new_investor_action"] = "AVOID"

    elif rec == "BUY":
        price_action["new_investor_action"] = "BUY_NOW"

    elif rec == "ACCUMULATE":
        if price_action["new_investor_action"] not in ["BUY_NOW", "WAIT"]:
            price_action["new_investor_action"] = "WAIT"

    elif rec == "HOLD":
        if price_action["holder_action"] not in ["HOLD", "WAIT"]:
            price_action["holder_action"] = "HOLD"

    return price_action