import pandas as pd


def calculate_technical_indicators(history: pd.DataFrame):

    
    history = history.dropna(subset=["Close"])

    print(history.tail())
    print("Current:", history["Close"].iloc[-1])

    close = history["Close"]

    # Moving averages
    sma_20 = close.rolling(20).mean()
    sma_50 = close.rolling(50).mean()
    sma_200 = close.rolling(200).mean()

    # RSI
    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    current_price = float(history["Close"].iloc[-1])
    
    sma20_value = sma_20.iloc[-1]
    sma50_value = sma_50.iloc[-1]
    sma200_value = sma_200.iloc[-1]
    rsi_value = rsi.iloc[-1]

    # Determine trend
    if (
        not pd.isna(sma200_value)
        and current_price > sma50_value > sma200_value
    ):
        trend = "BULLISH"

    elif (
        not pd.isna(sma200_value)
        and current_price < sma50_value < sma200_value
    ):
        trend = "BEARISH"

    else:
        trend = "NEUTRAL"

    return {
        "current_price": round(current_price, 2),

        "sma_20": (
            round(float(sma20_value), 2)
            if not pd.isna(sma20_value)
            else None
        ),

        "sma_50": (
            round(float(sma50_value), 2)
            if not pd.isna(sma50_value)
            else None
        ),

        "sma_200": (
            round(float(sma200_value), 2)
            if not pd.isna(sma200_value)
            else None
        ),

        "rsi_14": (
            round(float(rsi_value), 2)
            if not pd.isna(rsi_value)
            else None
        ),

        "trend": trend,
    }

# previously
# Price > SMA50 → bullish

# Now
# Price > SMA50 > SMA200
#         ↓
#      BULLISH
# and
# Price < SMA50 < SMA200
#         ↓
#      BEARISH

# This is still basic, but better.