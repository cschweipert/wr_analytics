from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, update, case, cast, Float

from models.models import Answer, Designer


class CleanAnswers:
    def __init__(self, db_session):
        self.db_session = db_session

    def delete_unknown_and_empty_answers(self):
        session = self.db_session()
        try:
            session.query(Answer).filter(
                (Answer.value == 'unknown') |
                (Answer.value == '') |
                (Answer.value is None) |
                (func.trim(Answer.value) == '')
            ).delete(synchronize_session=False)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def trim_and_clean_internal_whitespace(self):
        session = self.db_session()
        try:
            clean_expression = func.trim(func.regexp_replace(Answer.value, '\\s+', ' ', 'g'))
            session.query(Answer)\
                   .update({Answer.value: clean_expression}, synchronize_session=False)

            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update_values(self):
        session = self.db_session()
        try:
            updated_value = case(
                (Answer.value.like('+%'), func.substr(Answer.value, 2)),
                (Answer.value.like('.%'), '0' + func.substr(Answer.value, 1)),
                else_=Answer.value
            )
            session.query(Answer).update({Answer.value: updated_value}, synchronize_session='fetch')
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def inspect_weird_answers(self):
        """
        Method that inspects values out of order after applying sort
        during manual inspetion. 
        """
        criteria = [
            ("Sociedad de Acueducto, Alcantarillado y Aseo de Barranquilla", 1352),
            ("Wesfarmers Limited", 1180),
            ("Samsung Engineering", 1250),
        ]
        session = self.db_session()

        for company, metric_id in criteria:
            results = session.query(Answer).filter(
                Answer.company == company.lower(),
                Answer.metric_id == metric_id
            ).all()

            for result in results:
                print(f"Company: {result.company}, Metric ID: {result.metric_id}, Value: {result.value}, Type of Value: {type(result.value)}")
        session.close()

    def separate_numerical_and_non_numerical_values(self):
        session = self.db_session()
        try:
            answers = session.query(Answer).all()
            for answer in answers:
                try:
                    _ = float(answer.value)
                except ValueError:
                    answer.non_numerical = answer.value
                    answer.value = None
            session.commit()
        except IntegrityError as e:
            print(f"An error occurred: {e}")
            session.rollback()
        finally:
            session.close()

    def flag_negative_values(self):
        session = self.db_session()
        try:
            session.query(Answer).filter(
                cast(Answer.value, Float) < 0
            ).update({Answer.flag: True}, synchronize_session=False)

            session.commit()
            session.close()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def extract_designer(self):
        session = self.db_session()
        try:
            metrics_with_plus = session.query(Answer).filter(Answer.metric.contains('+')).all()
            for answer in metrics_with_plus:
                designer_name = answer.metric.split('+')[0].strip()
                designer = session.query(Designer).filter_by(name=designer_name).first()
                if not designer:
                    designer = Designer(name=designer_name)
                    session.add(designer)
                    session.commit()
                answer.designer_id = designer.id
                answer.metric = answer.metric.split('+', 1)[-1].strip()

            session.commit()
            session.close()
        except IntegrityError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def clean_and_transform_answers(self):
        self.delete_unknown_and_empty_answers()
        self.trim_and_clean_internal_whitespace()
        self.update_values()
        self.separate_numerical_and_non_numerical_values()
        self.flag_negative_values()
        self.extract_designer()