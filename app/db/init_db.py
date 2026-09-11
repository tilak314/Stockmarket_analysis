from app.db.database import Base, engine
from app.db.models import StockAnalysis


def init_db():
    Base.metadata.create_all(bind=engine)