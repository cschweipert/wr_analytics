from sqlalchemy.exc import IntegrityError

from models.answers import Answer, RawAnswer


class TransformAnswer:
    def __init__(self, db_session):
        self.db_session = db_session

    def query_raw_answers(self):
        session = self.db_session()
        try:
            query = session.query(
                RawAnswer.wr_id,
                RawAnswer.metric,
                RawAnswer.company,
                RawAnswer.value,
                RawAnswer.year,
            )
            results = query.all()
            return results
        finally:
            session.close()

    def insert_data(self, data_rows):
        session = self.db_session()
        try:
            for row in data_rows:
                wr_id = row[0]
                existing_data = session.query(Answer).filter_by(wr_id=wr_id).first()
                if not existing_data:
                    answer_data = {
                        'wr_id': row[0],
                        'metric': row[1].lower() if isinstance(row[1], str) else row[1],
                        'company': row[2].lower() if isinstance(row[2], str) else row[2],
                        'value': row[3].lower() if isinstance(row[3], str) else row[3],
                        'year': row[4]
                    }
                    answer_record = Answer(**answer_data)
                    session.add(answer_record)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def fetch_and_insert_data(self):
        raw_answers_data = self.query_raw_answers()
        self.insert_data(raw_answers_data)
