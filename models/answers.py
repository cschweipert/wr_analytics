from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from utils.sql_event_listeners import CustomBaseClass


class RawAnswer(CustomBaseClass):
    __tablename__ = 'raw_answers'

    id = Column(Integer, primary_key=True)
    wr_id = Column(Integer, nullable=False)
    metric = Column(String)
    company = Column(String)
    value = Column(String)
    year = Column(Integer)
    comments = Column(Text)
    sources = Column(JSONB)
    checked_by = Column(String)
    check_requested = Column(DateTime)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        )


class Answer(CustomBaseClass):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    wr_id = Column(Integer, nullable=False)
    metric = Column(String)
    company = Column(String)
    value = Column(String)
    year = Column(Integer)created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        )
