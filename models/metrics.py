from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

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
    value_options = Column(String)
    value_type = Column(String)
