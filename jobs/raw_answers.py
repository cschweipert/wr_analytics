from typing import List, Any
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from models.models import RawAnswer, RawMetric


DESIGNER = 'Global Reporting Initiative'


class InsertRawAnswer:
    def __init__(self, wr_api, db_session):
        self.wr_api = wr_api
        self.db_session = db_session

    def get_answers_by_designer(self, metric_name, metric_designer) -> List[Any]:  # noqa E501
        batch_size = 100
        offset = 0
        answers = []
        while True:
            batch_answers = self.wr_api.get_answers(
                limit=batch_size,
                offset=offset,
                metric_name=metric_name,
                metric_designer=metric_designer
                )
            answers.extend(batch_answers)
            serialized_raw_answers = self.serialize_raw_answers(answers)
            self.insert_raw_answers(serialized_raw_answers)
            offset += batch_size
            print(f'Fetched {len(batch_answers)} answers for metric {metric_name}. Total: {len(answers)}')  # TODO: replace with logging  # noqa E501
            if len(batch_answers) < batch_size:
                break
        return answers

    from sqlalchemy.future import select

    def fetch_metrics_name(self):
        session = self.db_session()
        try:
            stmt = select(RawMetric.name).where(RawMetric.designer == 'Global Reporting Initiative')
            results = session.execute(stmt).scalars().all()
            return results
        finally:
            session.close()

    def fetch_and_insert_answers(self):
        metrics = self.fetch_metrics_name()
        for metric in metrics:
            answers = self.get_answers_by_designer(metric_name=metric, metric_designer=DESIGNER)
            if len(answers) > 0:
                serialized_raw_answers = self.serialize_raw_answers(answers)
                self.insert_raw_answers(serialized_raw_answers)

    def serialize_raw_answers(self, answers):
        serialized_data = []
        for answer in answers:
            serialized_data.append({
                'wr_id': answer.id,
                'metric': answer.metric if hasattr(answer, 'metric') else None,
                'company': answer.company if hasattr(answer, 'company') else None,
                'value': str(answer.value) if hasattr(answer, 'value') else None,
                'year': answer.year if hasattr(answer, 'year') else None,
                'comments': answer.comments if hasattr(answer, 'comments') else None,
                'sources': answer.sources if hasattr(answer, 'sources') else None,
                'checked_by': answer.checked_by if hasattr(answer, 'checked_by') else None,
                'check_requested': answer.checked_requested if hasattr(answer, 'checked_requested') else None,
                'url': answer.url if hasattr(answer, 'url') else None,
            })
        return serialized_data

    def insert_raw_answers(self, serialized_answers):
        session = self.db_session()
        try:
            for answer_data in serialized_answers:
                wr_id = answer_data['wr_id']
                existing_answer = (
                    session.query(RawAnswer)
                    .filter_by(wr_id=wr_id)
                    .first()
                )
                if not existing_answer:
                    answer_data = {key: value if value is not None else None for key, value in answer_data.items()}  # noqa E501
                    answer = RawAnswer(**answer_data)
                    session.add(answer)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()
