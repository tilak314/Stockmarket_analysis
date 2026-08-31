from pydantic import BaseModel
from typing import List


class StockAnalysisRequest(BaseModel):
    ticker: str


class CurrentPriceAction(BaseModel):
    action: str
    reason: str
    holder_action: str
    new_investor_action: str


class StockScores(BaseModel):
    technical_score: int
    fundamental_score: int
    news_score: int
    market_score: int
    valuation_score: int
    final_stock_score: int


class StockRecommendation(BaseModel):

    recommendation: str

    confidence: int
    
    scores: StockScores

    short_term_outlook: str

    medium_term_outlook: str

    technical_summary: str

    fundamental_summary: str

    news_summary: str

    key_positives: List[str]

    key_risks: List[str]

    buy_zone_min: float | None = None

    buy_zone_max: float | None = None

    reconsider_if: List[str]

    probability_positive: int

    probability_negative: int

    probability_neutral: int

