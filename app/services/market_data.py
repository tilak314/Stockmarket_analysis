import yfinance as yf


def get_market_data():

    ticker = yf.Ticker("^NSEI")

    history = ticker.history(period="1y")

    history = history.dropna(subset=["Close"])

    close = history["Close"]

    current_price = float(close.iloc[-1])

    sma_50 = close.rolling(50).mean().iloc[-1]
    sma_200 = close.rolling(200).mean().iloc[-1]

    if current_price > sma_50 > sma_200:
        trend = "BULLISH"

    elif current_price < sma_50 < sma_200:
        trend = "BEARISH"

    else:
        trend = "NEUTRAL"

    return {
        "current_price": round(current_price, 2),
        "sma_50": round(float(sma_50), 2),
        "sma_200": round(float(sma_200), 2),
        "trend": trend
    }

print(get_market_data())