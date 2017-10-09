import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:

    @staticmethod
    def session(Base=None):
        connection_string = 'mysql+pymysql://%s:%s@%s:3306/%s' % (
            os.environ['GRADER_USER'],
            os.environ['GRADER_PASSWORD'],
            os.environ['GRADER_HOST'],
            os.environ['GRADER_DATABASE']
        )

        engine = create_engine(connection_string, echo=False)
        s = sessionmaker(bind=engine, expire_on_commit=False)
        if Base:
            Base.metadata.create_all(bind=engine)
        return s()
