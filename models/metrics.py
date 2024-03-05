from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from utils.sql_event_listeners import CustomBaseClass


class Metric(CustomBaseClass):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True)
    wr_id = Column(Integer)
    name = Column(String)
    designer = Column(String)
    metric_type = Column(String)
    unit = Column(String)
    answers = Column(Integer)
    bookmarkers = Column(Integer)
    value_type = Column(String)
    category = Column(String)
    env_category = Column(String)
    src_category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        )


class RawMetric(CustomBaseClass):
    __tablename__ = 'raw_metrics'

    id = Column(Integer, primary_key=True)
    wr_id = Column(Integer)
    name = Column(String)
    designer = Column(String)
    question = Column(Text)
    metric_type = Column(String)
    about = Column(Text)
    methodology = Column(Text)
    value_type = Column(String)
    value_options = Column(JSONB)
    report_type = Column(String)
    research_policy = Column(String)
    unit = Column(String)
    range = Column(String)
    hybrid = Column(String)
    topics = Column(JSONB)
    scores = Column(String)
    formula = Column(Text)
    answers = Column(Integer)
    bookmarkers = Column(Integer)
    projects = Column(String)
    answers_url = Column(String)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        )
