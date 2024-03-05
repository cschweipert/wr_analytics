from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

from jobs.metrics import Metrics
from models.metrics import Base
from wr_api import WikirateAPI

DATABASE_URL = config('DATABASE_URL')

app = FastAPI()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

wr_api = WikirateAPI(config('WR_API_KEY'))
metrics_data = Metrics(wr_api, SessionLocal)


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/fetch-metrics/')
def fetch_metrics():
    metrics = metrics_data.fetch_all_metrics()
    serialized_metrics = metrics_data.serialize_metrics(metrics)
    metrics_data.insert_metrics(serialized_metrics)
    return serialized_metrics
