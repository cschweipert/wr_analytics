from datetime import datetime
from sqlalchemy import event
from sqlalchemy.orm import Session as BaseSession
from sqlalchemy.orm.attributes import get_history
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CustomBaseClass(Base):
    __abstract__ = True

    @staticmethod
    def strip_whitespace_before_insert(mapper, connection, target):
        if hasattr(target, 'unit') and target.unit:
            target.unit = target.unit.strip()

    @staticmethod
    def strip_whitespace_before_update(mapper, connection, target):
        if hasattr(target, 'unit') and target.unit:
            target.unit = target.unit.strip()

    @staticmethod
    def before_update_listener(mapper, connection, target):
        session = BaseSession.object_session(target)
        if session is not None:
            if hasattr(target, 'unit'):
                history = get_history(target, 'unit')
                if history.has_changes():
                    target.updated_at = datetime.utcnow()


event.listen(CustomBaseClass, 'before_insert', CustomBaseClass.strip_whitespace_before_insert)  # noqa E501
event.listen(CustomBaseClass, 'before_update', CustomBaseClass.strip_whitespace_before_update)  # noqa E501
event.listen(CustomBaseClass, 'before_update', CustomBaseClass.before_update_listener)
