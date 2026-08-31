Foundation - - 

                FastAPI
                   │
                   ↓
             Stock Agent
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
   Stock Data   Technical     News
       │           │           │
       └───────────┼───────────┘
                   ↓
                Gemini
                   ↓
           Stock Analysis

What is correct?
GROWW.NS
   ↓
Yahoo Finance  -  stock_data.py
   ↓
Price + fundamentals + 1-year history  - stock_data["history"]
   ↓
Technical indicators
   ↓
News  - new_service.py
   ↓
Gemini
   ↓
Recommendation 

problems:

Problem 1 — Too much output
For a personal stock agent, we want something much cleaner.
GROWW
₹203.01

🟢 ACCUMULATE
Confidence: 75%

Short term: Neutral
Medium term: Positive

Buy zone: ₹190–195
Current price: ₹203

Technical: Bullish
Fundamental: Strong but expensive
News: Slightly Negative

Key positives:
• Strong growth
• Positive institutional activity

Key risks:
• Ribbit block deal
• High valuation

Important news:
1. Ribbit Capital block deal
2. Promoter pledge release
3. ...

Problem 2 - 
news service is giving broad results and some of them are duplicated - like same news reported by three publications.

Problem 3 -
For a company like Groww, we shouldn't blindly tell the LLM:

Problem 4 -
Gemini is inventing certainty

Look at:

Positive: 55%
Negative: 25%
Neutral: 20%

Where did those numbers come from?

There is no statistical model behind them.

Gemini essentially made up those probabilities based on its reasoning.

That's not acceptable for the final prediction system.

High D/E = high financial risk.

The LLM did exactly that.

It wrote:

"Debt/equity > 3 increases financial risk."

That may be a misinterpretation of the particular financial-data field.


Solution for foundation problems -
1. News strategy

Instead of 
Google News
    ↓
Give everything to Gemini

We will do this for news strategy
Google News
    ↓
Fetch ~10-15 recent articles
    ↓
Filter by date
    ↓
Remove duplicates (diff articles may be related to same event)
    ↓
Keep top 5
    ↓
Gemini

2. Stock data 
in stock_data.py we are passing the 1 year stock price history data of the stock to gemini - json.dumps(stock_data, default=str)
That means we're potentially sending hundreds of price rows to Gemini.

There is absolutely no need.

Gemini only needs the calculated indicators.

change stock service arch to below
Raw market data
       ↓
Python calculations
       ↓
Small structured dataset
       ↓
Gemini


New architecture
             GROWW.NS
                 │
       ┌─────────┴─────────┐
       ↓                   ↓
  Yahoo Finance        Google News
       │                   │
       ↓                   ↓
  Price/history       10-15 articles
       │                   │
       ↓                   ↓
 Technical calc       Filter + dedupe
       │                   │
       ↓                   ↓
 Technical summary      Top 5 news
       │                   │
       └─────────┬─────────┘
                 ↓
              Gemini
                 ↓
          Structured output
                 ↓
          BUY / HOLD / SELL


Improving scores steps - 
Stock Data
   ↓
Technical Indicators
   ↓
Technical Score
   ↓
Fundamental Score
   ↓
News Score
   ↓
Market Score
   ↓
Valuation Score
   ↓
Final Stock Score
   ↓
Score-based Recommendation
   ↓
BUY / ACCUMULATE / HOLD / AVOID / SELL
   ↓
Current Price Action
   ├── holder_action
   └── new_investor_action
Final cleanup + testing with Groww, TMCV, Apollo, BEL


for improving recommendations
Scores
   ↓
Baseline Recommendation
   ↓
Gemini analysis - decision.py
   ↓
Final Recommendation
   ↓
Final consistency validation  ← NEXT - decision_validator.py


Stock Data
    ↓
Technical calculations
    ↓
Support / resistance / valuation
    ↓
Buy-zone calculation
    ↓
LLM
    ↓
Recommendation
    ↓
Current-price action

# instead of asking LLm to generate tech score, we use price, smi_20, smi_50, smi_200 to generate some score - check scoring.py and pass that to LLM prompt

Phase 1 — Make the analysis reliable

Better technical indicators
Better news collection
News sentiment + impact
Fundamental scoring
Market/NIFTY context
Combine everything into a numerical stock score
BUY/HOLD/SELL decision

Phase 2 — Make it actually predictive

Record every prediction
Check what happened afterward
Calculate prediction accuracy
Build historical dataset
Eventually train a simple ML model
Compare ML prediction vs LLM analysis

Phase 3 — Personal agent

Watchlist
Your holdings
Buy-zone detection
Sell alerts
Daily stock report
Scheduled news monitoring