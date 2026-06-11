from sqlalchemy import Column, Integer, String, DateTime
from backend.database import Base
import datetime

class Candidate(Base):
    """Модель таблицы кандидатов"""
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, default="")
    votes = Column(Integer, default=0)

class Vote(Base):
    """Модель таблицы голосов"""
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_ip = Column(String, nullable=False)
    candidate_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))