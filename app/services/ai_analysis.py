import os
import json

from dotenv import load_dotenv
from google import genai

from app.models.stock_models import StockRecommendation
from anthropic import Anthropic
from openai import OpenAI
from google.genai import types
from app.services.agent_tools import get_stock_price

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

client2 = Anthropic(
    api_key=os.getenv("ANTHROPIC_KEY")
)


client3 = OpenAI(
    api_key=os.getenv("OPENAI_KEY")
)



def ask_rag(question, context):

    prompt = f"""
        Answer the user's question using only the provided context.

        Context:
        {chr(10).join(context)}

        Question:
        {question}
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


def analyze_stock(
    stock_data,
    technical_data,
    news_data, 
    technical_score,
    fundamental_score,
    news_score,
    valuation_score, 
    market_score,
    final_stock_score,
    score_recommendation,
    buy_zone_min,
    buy_zone_max
):

    prompt = f"""
You are a stock market research assistant.

Analyze the stock using ONLY the supplied data.
Do not invent missing information.
Do not guarantee future price movements.
This is investment research, not financial advice.

STOCK DATA:
{json.dumps(stock_data, indent=2, default=str)}

TECHNICAL DATA:
{json.dumps(technical_data, indent=2, default=str)}

NEWS:
{json.dumps(news_data, indent=2, default=str)}

CALCULATED SCORES:
These scores are calculated by Python. Do NOT recalculate them.

Technical: {technical_score}
Fundamental: {fundamental_score}
News: {news_score}
Market: {market_score}
Valuation: {valuation_score}
Final: {final_stock_score}

BASE RECOMMENDATION:
{score_recommendation}

Use this as the baseline recommendation.
Change it only when the supplied evidence strongly contradicts it.

RECOMMENDATION:
Choose one:
BUY, ACCUMULATE, HOLD, AVOID, SELL

CONFIDENCE:
0-100.


OUTLOOK:
short_term_outlook: POSITIVE, NEUTRAL, NEGATIVE
medium_term_outlook: POSITIVE, NEUTRAL, NEGATIVE

ANALYSIS:
Provide concise:
- technical summary
- fundamental summary
- news summary
- maximum 3 positives
- maximum 3 risks

BUY ZONE:
Python has calculated the potential buy zone:

Min: {buy_zone_min}
Max: {buy_zone_max}

Use these values.
Do not invent or recalculate the buy zone.
If both are null, return null.

RECONSIDERATION:
Give up to 4 conditions that could change the recommendation.

PROBABILITIES:
positive_probability + negative_probability + neutral_probability
must equal exactly 100.

Keep all explanations concise.
"""
    response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config={
            "response_mime_type": "application/json",
            "response_schema": StockRecommendation,
        },
    )

    return StockRecommendation.model_validate_json(
        response.text
    )

    # ANTHROPIC

    # response = client.messages.create(
    #     model="claude-sonnet-5",
    #     max_tokens=2000,
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #     ],
    #     output_config={
    #         "format": {
    #             "type": "json_schema",
    #             "schema": StockRecommendation.model_json_schema()
    #         }
    #     }
    # )

    # OPEN AI code 

    # response = client3.responses.parse(
    #     model="gpt-5.5",
    #     input=prompt,
    #     text_format=StockRecommendation,
    # )

    # result = response.output_parsed
    # return result


stock_price_tool = types.FunctionDeclaration(
    name="get_stock_price",
    description="Get the current stock price and company name.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "ticker": {
                "type": "STRING",
                "description": "Stock ticker symbol, e.g. BEL.NS"
            }
        },
        "required": ["ticker"]
    }
)

def run_agent(question):

    tool = types.Tool(
        function_declarations=[stock_price_tool]
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=question,
        config=types.GenerateContentConfig(
            tools=[tool]
        )
    )

    return response