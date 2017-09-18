from Database import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float


Base = declarative_base()
class TestResult(Base):
    __tablename__ = 'testresults'

    id = Column(Integer, primary_key=True)
    submission_id_program = Column(Integer)
    submission_id_test = Column(Integer)
    tests = Column(Integer)
    errors = Column(Integer)
    failures = Column(Integer)
    coverage = Column(Float)
    time = Column(Integer)


    def __init__(self, submission_id_program, submission_id_test, tests, errors, failures, coverage, time):
        self.submission_id_program = submission_id_program
        self.submission_id_test = submission_id_test
        self.tests = tests
        self.errors = errors
        self.failures = failures
        self.coverage = coverage
        self.time = time

session = Database.session(Base)
session.close()
