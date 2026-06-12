from sqlalchemy import Column, Integer, String, DateTime, Index, Boolean
from backend.database import Base
import datetime

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, default="")
    votes = Column(Integer, default=0)

class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    user_ip = Column(String, nullable=False, index=True)
    candidate_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    __table_args__ = (Index('ix_votes_ip_candidate', 'user_ip', 'candidate_id'),)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)