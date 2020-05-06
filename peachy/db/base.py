from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from peachy.settings import get_setting


engine = create_engine(get_setting("db_connection_string"))
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


@contextmanager
def scoped_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
