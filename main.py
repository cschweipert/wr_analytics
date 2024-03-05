from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

from jobs.raw_metrics import InsertRawMetric
from jobs.answers_gri_env import TransformAnswer
from jobs.clean_metrics import CleanMetric
from jobs.raw_answers_gri_env import InsertRawAnswer
from utils.sql_event_listeners import Base
from wr_api import WikirateAPI

DATABASE_URL = config('DATABASE_URL')

app = FastAPI()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

wr_api = WikirateAPI(config('WR_API_KEY'))

raw_metrics_data = InsertRawMetric(wr_api, SessionLocal)
raw_answers_data = InsertRawAnswer(wr_api, SessionLocal)
clean_metrics = CleanMetric(wr_api, SessionLocal)
answers_data = TransformAnswer(SessionLocal)


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/raw-metrics/')
def fetch_and_insert_raw_metrics():
    raw_metrics_data.fetch_and_insert_metrics()


@app.get('/raw-answers/')
def fetch_and_insert_raw_answers():
    raw_answers_data.fetch_and_insert_answers()


@app.get('/gri-answers/')
def fetch_and_insert_gri_answers():
    answers_data.fetch_and_insert_data()


@app.get('/clean-metrics/')
def transform_metrics_data():
    clean_metrics.update_to_lowercase_and_remove_whitespace()  # noqa E501
