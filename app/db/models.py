from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from app.db.database import Base


class StockAnalysis(Base):
    __tablename__ = "stock_analyses"

    id = Column(Integer, primary_key=True, index=True)

    ticker = Column(String, index=True, nullable=False)
    company = Column(String, nullable=True)

    current_price = Column(Float, nullable=True)

    recommendation = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)

    risk_level = Column(String, nullable=True)
    stop_loss = Column(Float, nullable=True)

    technical_score = Column(Float, nullable=True)
    fundamental_score = Column(Float, nullable=True)
    news_score = Column(Float, nullable=True)
    market_score = Column(Float, nullable=True)
    valuation_score = Column(Float, nullable=True)
    final_score = Column(Float, nullable=True)

    analysis_data = Column(JSON, nullable=True)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )