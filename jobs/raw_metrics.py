from sqlalchemy.exc import IntegrityError

from models.metrics import RawMetric
from utils.globals import METRIC_DESIGNERS


class InsertRawMetric:
    def __init__(self, wr_api, db_session):
        self.wr_api = wr_api
        self.db_session = db_session

    def get_metrics_by_designer(self, metric_designer):
        batch_size = 100
        offset = 0
        metrics = []
        while True:
            batch_metrics = self.wr_api.get_metrics(
                limit=batch_size,
                offset=offset,
                metric_designer=metric_designer
                )
            metrics.extend(batch_metrics)
            offset += batch_size
            print(f'Fetched {len(batch_metrics)} metrics for designer {metric_designer}. Total: {len(metrics)}')  # TODO: replace with logging
            if len(batch_metrics) < batch_size:
                break
        return metrics

    def fetch_and_insert_metrics(self):
        for designer in METRIC_DESIGNERS:
            metrics = self.get_metrics_by_designer(designer)
            if len(metrics) > 0:
                serialized_raw_metrics = self.serialize_raw_metrics(metrics)
                self.insert_raw_metrics(serialized_raw_metrics)

    def serialize_raw_metrics(self, metrics):
        serialized_metrics = []
        for metric in metrics:
            serialized_metric = {
                'wr_id': metric.id,
                'name': metric.name if hasattr(metric, 'name') else None,
                'designer': metric.designer if hasattr(metric, 'designer') else None,
                'question': metric.question if hasattr(metric, 'question') else None,
                'metric_type': metric.metric_type if hasattr(metric, 'metric_type') else None,
                'about': metric.about if hasattr(metric, 'about') else None,
                'methodology': metric.methodology if hasattr(metric, 'methodology') else None,
                'value_type': metric.value_type if hasattr(metric, 'value_type') else None,
                'value_options': metric.value_options if hasattr(metric, 'value_options') else None,
                'report_type': metric.report_type if hasattr(metric, 'report_type') else None,
                'research_policy': metric.research_policy if hasattr(metric, 'research_policy') else None,
                'unit': metric.unit if hasattr(metric, 'unit') else None,
                'range': metric.range if hasattr(metric, 'range') else None,
                'hybrid': metric.hybrid if hasattr(metric, 'hybrid') else None,
                'topics': metric.topics if hasattr(metric, 'topics') else None,
                'scores': metric.scores if hasattr(metric, 'scores') else None,
                'formula': metric.formula if hasattr(metric, 'formula') else None,
                'answer_count': metric.answers if hasattr(metric, 'answers') else None,
                'bookmarkers': metric.bookmarkers if hasattr(metric, 'bookmarkers') else None,
                'projects': metric.projects if hasattr(metric, 'projects') else None,
                'calculations': metric.calculations if hasattr(metric, 'calculations') else None,
                'answers_url': metric.answers_url if hasattr(metric, 'answers_url') else None,
                'url': metric.url if hasattr(metric, 'url') else None,
            }

            serialized_metrics.append(serialized_metric)
        return serialized_metrics

    def insert_raw_metrics(self, serialized_metrics):
        session = self.db_session()
        try:
            for metric_data in serialized_metrics:
                wr_id = metric_data['wr_id']
                existing_metric = (
                    session.query(RawMetric)
                    .filter_by(wr_id=wr_id)
                    .first()
                )
                if not existing_metric:
                    metric_data = {key: value if value is not None else None for key, value in metric_data.items()}  # noqa E501
                    metric = RawMetric(**metric_data)
                    session.add(metric)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()
