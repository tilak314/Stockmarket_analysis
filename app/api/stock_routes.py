from fastapi import APIRouter, HTTPException
from app.workers.tasks import analyze_stock_task
from celery.result import AsyncResult
from app.workers.celery_app import celery

from app.models.stock_models import StockAnalysisRequest

from app.services.stock_data import get_stock_data
from app.services.technical_analysis import calculate_technical_indicators
from app.services.news_service import get_company_news
from app.services.ai_analysis import analyze_stock
from app.services.scoring import calculate_technical_score, calculate_fundamental_score, calculate_news_score, calculate_valuation_score, calculate_market_score, calculate_final_stock_score, get_score_recommendation, calculate_buy_zone
from app.services.market_data import get_market_data
from app.services.decision_validator import validate_decision
from app.services.decision import get_price_action
from app.services.risk import calculate_risk_level, calculate_stop_loss
from app.services.cache import get_cached_analysis, set_cached_analysis

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):

    result = AsyncResult(task_id, app=celery)

    if result.state == "PENDING":
        return {
            "task_id": task_id,
            "status": "processing"
        }

    if result.state == "SUCCESS":
        return {
            "task_id": task_id,
            "status": "completed",
            "result": result.result
        }

    if result.state == "FAILURE":
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(result.result)
        }

    return {
        "task_id": task_id,
        "status": result.state
    }

@router.post("/analyze")
def analyze(request: StockAnalysisRequest):

    ticker = request.ticker.upper().strip()

    cached_result = get_cached_analysis(ticker)

    if cached_result:
        print("cached result")
        return {
            "status": "cached",
            "result": cached_result
        }
    print("not cached")

    task = analyze_stock_task.delay(ticker)

    return {
        "task_id": task.id,
        "ticker": ticker,
        "status": "processing"
    }


# @router.post("/analyze")
# def analyze(request: StockAnalysisRequest):

#     try:

#         ticker = request.ticker.upper().strip()

#         cached_result = get_cached_analysis(ticker)
        
#         if cached_result:
#             print("cached data")
#             return cached_result

#         # 1. Get stock data
#         stock_data, history = get_stock_data(
#             ticker
#         )

#         # 2. Technical analysis
#         technical_data = calculate_technical_indicators(
#             history
#         )

#         # 3. News
#         news_data = get_company_news(
#             company_name=stock_data["company_name"],
#             ticker=ticker,
#             limit=5,
#             days=7
#         )

#         # scores
#         # 1. technical score
#         technical_score = calculate_technical_score(
#             price=technical_data["current_price"],
#             sma_20=technical_data["sma_20"],
#             sma_50=technical_data["sma_50"],
#             sma_200=technical_data["sma_200"],
#             rsi=technical_data["rsi_14"]
#         )
#         print("technical_score - ", technical_score)

#         # 2. fundamental score
#         fundamental_score = calculate_fundamental_score(
#             revenue_growth=stock_data["revenue_growth"],
#             profit_margin=stock_data["profit_margin"],
#             roe=stock_data["roe"],
#             roa=stock_data["roa"],
#             debt_to_equity=stock_data["debt_to_equity"]
#         )
#         print("fundamental_score - ", fundamental_score)


#         # 3. NEWS SCORE
#         news_score = calculate_news_score(news_data)
#         print("news_score - ", news_score)


#         # 4. valution score
#         valuation_score = calculate_valuation_score(
#             pe_ratio=stock_data["pe_ratio"],
#             forward_pe=stock_data["forward_pe"],
#             revenue_growth=stock_data["revenue_growth"]
#         )

#         print("valuation_score - ", valuation_score)


#         # 5. Market score
#         market_score = calculate_market_score(
#             current_price=technical_data["current_price"],
#             sma_50=technical_data["sma_50"],
#             sma_200=technical_data["sma_200"],
#             trend=technical_data["trend"]
#         )

#         # final weighted score
#         final_stock_score = calculate_final_stock_score(
#             technical_score=technical_score,
#             fundamental_score=fundamental_score,
#             news_score=news_score,
#             market_score=market_score,
#             valuation_score=valuation_score
#         )

#         print("final_stock_score - ", final_stock_score)

#         score_recommendation = get_score_recommendation(
#             final_stock_score
#         )

#         print("score_recommendation - ", score_recommendation)


#         buy_zone_min, buy_zone_max = calculate_buy_zone(
#             price=technical_data["current_price"],
#             sma_20=technical_data["sma_20"],
#             sma_50=technical_data["sma_50"],
#             sma_200=technical_data["sma_200"]
#         )

#         risk_level = calculate_risk_level(
#             price=technical_data["current_price"],
#             sma_50=technical_data["sma_50"],
#             sma_200=technical_data["sma_200"],
#             rsi=technical_data["rsi_14"],
#             debt_to_equity=stock_data["debt_to_equity"]
#         )

#         stop_loss = calculate_stop_loss(
#             price=technical_data["current_price"],
#             sma_50=technical_data["sma_50"],
#             sma_200=technical_data["sma_200"]
#         )

#         print("risk_level - ", risk_level)
#         print("stop_loss - ", stop_loss)

        


#         #  AI analysis
#         recommendation = analyze_stock(
#             stock_data=stock_data,
#             technical_data=technical_data,
#             news_data=news_data,
#             technical_score=technical_score, 
#             fundamental_score =fundamental_score,
#             news_score = news_score,
#             valuation_score= valuation_score,
#             market_score= market_score,
#             final_stock_score = final_stock_score,
#             score_recommendation=score_recommendation,
#             buy_zone_min=buy_zone_min,
#             buy_zone_max=buy_zone_max
#         )

#         price_action = get_price_action(
#             recommendation=recommendation.recommendation,
#             current_price=technical_data["current_price"],
#             buy_zone_min=recommendation.buy_zone_min,
#             buy_zone_max=recommendation.buy_zone_max
#         )


#         # Validate Gemini's decision
#         price_action = validate_decision(
#             recommendation,
#             price_action
#         )
#         print("price action - ", price_action)

#         result = {
#             "ticker": ticker,

#             "company": stock_data["company_name"],

#             "price": technical_data["current_price"],

#             "recommendation": recommendation.model_dump(),

#             "current_price_action": price_action,

#             "risk": {
#                 "risk_level": risk_level,
#                 "stop_loss": stop_loss
#             },

#             "technical": technical_data,

#             "news": news_data
#         }
#         print("before")
#         set_cached_analysis(
#             ticker,
#             result,
#             ttl=3600
#         )
#         print("after cache")

#         return result
        

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )