from app.db.database import SessionLocal
from app.db.models import StockAnalysis


def save_analysis(data):
    import os
    db = SessionLocal()

    try:
        recommendation = data.get("recommendation", {})
        risk = data.get("risk", {})
        scores = data.get("scores", {})

        record = StockAnalysis(
            ticker=data["ticker"],
            company=data.get("company"),
            current_price=data.get("price"),

            recommendation=recommendation.get("recommendation"),
            confidence=recommendation.get("confidence"),

            risk_level=risk.get("risk_level"),
            stop_loss=risk.get("stop_loss"),

            technical_score=scores.get("technical_score"),
            fundamental_score=scores.get("fundamental_score"),
            news_score=scores.get("news_score"),
            market_score=scores.get("market_score"),
            valuation_score=scores.get("valuation_score"),
            final_score=scores.get("final_score"),

            analysis_data=data
        )

        db.add(record)
        db.commit()
        db.refresh(record)
        import os

        print("Row inserted")

        return record.id

    finally:
        db.close()