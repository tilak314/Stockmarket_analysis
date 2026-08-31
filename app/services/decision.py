def get_price_action(
    recommendation,
    current_price,
    buy_zone_min,
    buy_zone_max
):
    if recommendation == "BUY":
        if buy_zone_min is not None and current_price <= buy_zone_max:
            return {
                "action": "BUY_NOW",
                "holder_action": "HOLD",
                "new_investor_action": "BUY_NOW"
            }

        return {
            "action": "WAIT",
            "holder_action": "HOLD",
            "new_investor_action": "WAIT"
        }

    if recommendation == "ACCUMULATE":
        if (
            buy_zone_min is not None
            and buy_zone_max is not None
            and buy_zone_min <= current_price <= buy_zone_max
        ):
            return {
                "action": "BUY_NOW",
                "holder_action": "ACCUMULATE",
                "new_investor_action": "BUY_NOW"
            }

        return {
            "action": "WAIT",
            "holder_action": "HOLD",
            "new_investor_action": "WAIT"
        }

    if recommendation == "HOLD":
        return {
            "action": "HOLD",
            "holder_action": "HOLD",
            "new_investor_action": "WAIT"
        }

    if recommendation == "SELL":
        return {
            "action": "SELL",
            "holder_action": "SELL",
            "new_investor_action": "AVOID"
        }

    if recommendation == "AVOID":
        return {
            "action": "WAIT",
            "holder_action": "HOLD",
            "new_investor_action": "AVOID"
        }

    return {
        "action": "WAIT",
        "holder_action": "HOLD",
        "new_investor_action": "WAIT"
    }