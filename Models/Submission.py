from Core.Database import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, desc


Base = declarative_base()


class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    student_id = Column(String(50))
    problem_id = Column(String(50))
    program = Column(Text)
    test = Column(Text)
    error = Column(Boolean)

    def __init__(self, timestamp, student_id, problem_id, program, test, error):
        self.timestamp = timestamp
        self.student_id = student_id
        self.problem_id = problem_id
        self.program = program
        self.test = test
        self.error = error

    @staticmethod
    def get_last_submissions_each_user(problem_id):
        session = Database.session()
        student_ids = [s[0] for s in set(session.query(Submission.student_id))]

        submissions = [session.query(Submission).filter(
            Submission.student_id == s,
            Submission.problem_id == problem_id,
            Submission.error == False).order_by(desc(Submission.timestamp)).first()
            for s in student_ids]

        session.close()
        return [s for s in submissions if s is not None]

    @staticmethod
    def get_submission_user(student_id, problem_id):
        session = Database.session()
        s = session.query(Submission).filter(Submission.student_id == student_id, Submission.problem_id == problem_id).first()
        session.close()
        return s


session = Database.session(Base)
session.close()
