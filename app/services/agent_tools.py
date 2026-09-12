from app.services.stock_data import get_stock_data


def get_stock_price(ticker: str):
    stock_data, _ = get_stock_data(ticker)

    return {
        "ticker": ticker,
        "company": stock_data["company_name"],
        "price": stock_data["current_price"]
    }