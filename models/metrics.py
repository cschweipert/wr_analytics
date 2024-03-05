from sqlalchemy import Column, Integer, String, DateTime, event
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Metric(Base):
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
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        )


@event.listens_for(Metric, 'before_update')
def before_update_listener(mapper, connection, target):
    target.updated_at = datetime.utcnow()
