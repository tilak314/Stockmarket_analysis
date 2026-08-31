                    ┌──────────────────┐
                    │   POST /analyze  │
                    │  ticker: TMCV.NS │
                    └────────┬─────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │    stock_data.py    │
                  │                     │
                  │ Price               │
                  │ Fundamentals        │
                  │ PE / Forward PE     │
                  │ Revenue / Margin    │
                  │ Debt / ROE / ROA    │
                  │ Price History       │
                  └─────────┬───────────┘
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
   ┌──────────────────┐          ┌──────────────────┐
   │technical_analysis│          │   news_service   │
   │                  │          │                  │
   │ SMA20            │          │ Latest news      │
   │ SMA50            │          │ Company news     │
   │ SMA200           │          │                  │
   │ RSI              │          └────────┬─────────┘
   │ Trend             │                   │
   └────────┬─────────┘                   │
            │                             │
            ▼                             ▼
   ┌────────────────────────────────────────────┐
   │                  scoring.py                 │
   │                                            │
   │ Technical Score                            │
   │ Fundamental Score                          │
   │ News Score                                 │
   │ Valuation Score                            │
   │ Market Score                               │
   │                                            │
   │          ↓                                 │
   │ Final Weighted Score                       │
   │          ↓                                 │
   │ Score Recommendation                       │
   │          ↓                                 │
   │ Buy Zone                                   │
   └───────────────────┬────────────────────────┘
                       │
          ┌────────────┼─────────────┐
          ▼            ▼             ▼
    ┌──────────┐ ┌────────────┐ ┌────────────┐
    │ decision │ │   risk.py  │ │   Gemini   │
    │   .py    │ │            │ │            │
    │          │ │ Risk level │ │ Final      │
    │ BUY_NOW  │ │ Stop loss  │ │ analysis   │
    │ WAIT     │ │            │ │            │
    │ HOLD     │ │            │ │            │
    │ SELL     │ │            │ │            │
    └────┬─────┘ └─────┬──────┘ └─────┬──────┘
         │              │              │
         └──────────────┼──────────────┘
                        ▼
              ┌─────────────────────┐
              │ decision_validator  │
              │                     │
              │ Ensure recommendation│
              │ and action don't     │
              │ contradict           │
              └──────────┬──────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   Final JSON     │
                │                  │
                │ Recommendation   │
                │ Price Action     │
                │ Scores           │
                │ Risk             │
                │ Technical        │
                │ News             │
                └──────────────────┘


Next:
Phase 1 — Improve Risk Management
Risk Level
    ↓
Stop Loss
    ↓
Risk/Reward
    ↓
Position Size

Phase 2 — Make the Decision Engine smarter

Phase 3 — Reduce Gemini dependency
Move to below path
Python
    ↓
Calculations
    ↓
Decision Engine
    ↓
Gemini
    ↓
Explanation only

Instead of 
Python → Gemini decides everything


Phase 4 — Backtesting

This is a very important step.

We'll test:

Historical stock data
       ↓
Your scoring system
       ↓
Your decision system
       ↓
Would the decision have worked?


Phase 5 - Prod architecture
FastAPI
   ↓
Service Layer
   ↓
Scoring Engine
   ↓
Decision Engine
   ↓
Redis Cache
   ↓
Celery Workers - moving heavy/slow stock analysis out of the FastAPI request. Using this returns task id quickly
   ↓
Database
   ↓
Scheduled analysis
