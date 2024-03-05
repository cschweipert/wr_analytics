from sqlalchemy.exc import IntegrityError
from models.metrics import Metric

METRIC_DESIGNERS = [
    'Research Group Eticonsum',
    'Fashion Revolution',
    'Higher Education Statistics Agency (HESA)',
    'World Benchmarking Alliance',
    'Global Reporting Initiative',
    'US Securities and Exchange Commission',
    'Clean Clothes Campaign'
    ]


class Metrics:
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
            if len(batch_metrics) < batch_size:
                break
        return metrics

    def fetch_all_metrics(self):
        for designer in METRIC_DESIGNERS:
            metrics = self.get_metrics_by_designer(designer)
            if len(metrics) > 0:
                serialized_metrics = self.serialize_metrics(metrics)
                self.insert_metrics(serialized_metrics)

    def serialize_metrics(self, metrics):
        serialized_metrics = []
        for metric in metrics:
            serialized_metric = {
                'wr_id': metric.id,
                'name': metric.name,
                'designer': metric.designer,
                'metric_type': metric.metric_type,
                'unit': metric.unit,
                'answers': metric.answers,
                'bookmarkers': metric.bookmarkers,
                'value_type': metric.value_type
            }
            serialized_metrics.append(serialized_metric)
        return serialized_metrics

    def insert_metrics(self, serialized_metrics):
        session = self.db_session()
        try:
            for metric_data in serialized_metrics:
                wr_id = metric_data['wr_id']
                existing_metric = (
                    session.query(Metric)
                    .filter_by(wr_id=wr_id)
                    .first()
                )
                if not existing_metric:
                    metric = Metric(**metric_data)
                    session.add(metric)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()
