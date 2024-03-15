from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from utils.sql_event_listeners import CustomBaseClass


class Metric(CustomBaseClass):
    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True)
    wr_id = Column(Integer)
    name = Column(String)
    designer = Column(String)
    metric_type = Column(String)
    unit = Column(String)
    answer_count = Column(Integer)
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
    answer_count = Column(Integer)
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
    non_numerical = Column(String)
    year = Column(Integer)
    flag = Column(Boolean)
    metric_id = Column(Integer, ForeignKey('metrics.id'))
    metric_relation = relationship("Metric", backref="answers")
    designer_id = Column(Integer, ForeignKey('designers.id'), nullable=True)
    designer = relationship("Designer", backref="answers") 
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        )


class Designer(CustomBaseClass):
    __tablename__ = 'designers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
