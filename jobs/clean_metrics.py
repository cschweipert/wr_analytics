from typing import List
from sqlalchemy import update, func
from sqlalchemy.exc import SQLAlchemyError

from models.models import Metric
from utils.globals import ENVIRONMENTAL_UNITS, SOCIAL_UNITS


class CleanMetric:
    def __init__(self, wr_api, db_session_factory):
        self.wr_api = wr_api
        self.db_session_factory = db_session_factory

    def update_to_lowercase_and_remove_whitespace(self):
        try:
            session = self.db_session_factory()
            stmt = update(Metric).values(unit=func.lower(func.trim(Metric.unit)))
            session.execute(stmt)
            stmt = update(Metric).values(metric_type=func.lower(func.trim(Metric.metric_type)))
            session.execute(stmt)
            stmt = update(Metric).values(value_type=func.lower(func.trim(Metric.value_type)))
            session.execute(stmt)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def fetch_numeric_researched_metrics(self) -> List[Metric]:
        try:
            with self.db_session_factory() as session:
                researched_metrics = (
                    session.query(Metric)
                    .filter(
                        Metric.metric_type == 'researched',
                        Metric.value_type == 'number'
                    )
                    .all()
                )
                return researched_metrics
        except SQLAlchemyError as e:
            raise RuntimeError('Failed to fetch numeric researched metrics') from e

    def standardize_units_of_num_researched_metrics(self) -> None:
        try:
            with self.db_session_factory() as session:
                researched_metrics = self.fetch_numeric_researched_metrics()
                for metric in researched_metrics:
                    if metric.unit == 'tonnes co2 equivalent':
                        metric.unit = 'tonnes co2e'
                    elif metric.unit == 'metric tonnes':
                        metric.unit = 'tonnes'
                    elif metric.unit == 'cubic metres':
                        metric.unit = 'm3'
                    elif metric.unit is None:
                        metric.unit = 'fatalities'

                session.add_all(researched_metrics)
                session.commit()
        except SQLAlchemyError as e:
            raise RuntimeError('Failed to standardize units of researched metrics') from e

    def label_metrics_with_categories(self) -> None:
        try:
            with self.db_session_factory() as session:
                metrics = self.fetch_numeric_researched_metrics()
                for metric in metrics:
                    if metric.unit in ENVIRONMENTAL_UNITS:
                        metric.category = 'environmental'
                    elif 'environmental' in metric.name.lower():
                        metric.category = 'environmental'

                    if metric.unit == 'tonnes co2e':
                        metric.env_category = 'ghg_emissions'
                    elif metric.unit == 'gigajoules':
                        metric.env_category = 'energy_consumption'
                    elif 'water' in metric.name.lower():
                        metric.env_category = 'water'
                    elif 'waste' in metric.name.lower():
                        metric.env_category = 'waste'
                    elif 'emissions' in metric.name.lower() and metric.unit == 'tonnes':
                        metric.env_category = 'criteria_pollutants'

                    if metric.env_category is not None:
                        metric.category = 'environmental'

                    if metric.unit in SOCIAL_UNITS:
                        metric.category = 'social'

                session.add_all(metrics)
                session.commit()
        except SQLAlchemyError as e:
            raise RuntimeError('Failed to label metrics with categories') from e
