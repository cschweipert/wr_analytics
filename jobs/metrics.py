from sqlalchemy.exc import IntegrityError

from models.metrics import Metric, RawMetric


class TransformMetrics:
    def __init__(self, db_session):
        self.db_session = db_session

    def query_raw_metrics(self):
        session = self.db_session()
        try:
            query = session.query(
                RawMetric.wr_id, 
                RawMetric.name, 
                RawMetric.designer, 
                RawMetric.metric_type, 
                RawMetric.unit, 
                RawMetric.answers, 
                RawMetric.bookmarkers, 
                RawMetric.value_type
            )
            results = query.all()
            return results
        finally:
            session.close()

    def insert_metrics(self, data_rows):
        session = self.db_session()
        try:
            for row in data_rows:
                wr_id = row[0]
                existing_data = session.query(Metric).filter_by(wr_id=wr_id).first()
                if not existing_data:
                    answer_data = {
                        'wr_id': row[0],
                        'name': row[1].lower() if isinstance(row[1], str) else row[1],
                        'designer': row[2].lower() if isinstance(row[2], str) else row[2],
                        'metric_type': row[3].lower() if isinstance(row[3], str) else row[3],
                        'unit': row[4].lower() if isinstance(row[4], str) else row[4],
                        'answer_count': row[5].lower() if isinstance(row[5], str) else row[5],
                        'bookmarkers': row[6],
                        'value_type': row[7].lower() if isinstance(row[7], str) else row[7],
                    }
                    answer_record = Metric(**answer_data)
                    session.add(answer_record)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def fetch_and_insert_data(self):
        raw_metrics_data = self.query_raw_metrics()
        self.insert_metrics(raw_metrics_data)
