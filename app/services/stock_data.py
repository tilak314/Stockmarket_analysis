import yfinance as yf


def get_stock_data(ticker: str):

    ticker = ticker.upper().strip()

    stock = yf.Ticker(ticker)

    # Get enough history for long-term indicators
    history = stock.history(period="5y")

    if history.empty:
        raise ValueError(f"No stock data found for {ticker}")

    info = stock.info

    current_price = float(history["Close"].iloc[-1])

    stock_data = {
        "ticker": ticker,
        "company_name": info.get("longName") or ticker,

        "current_price": round(current_price, 2),

        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),

        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),

        "market_cap": info.get("marketCap"),

        "revenue_growth": info.get("revenueGrowth"),
        "profit_margin": info.get("profitMargins"),

        "roe": info.get("returnOnEquity"),
        "roa": info.get("returnOnAssets"),

        "debt_to_equity": info.get("debtToEquity"),

        "latest_trading_date": (
            history.index[-1].strftime("%Y-%m-%d")
        ),
    }

    return stock_data, history