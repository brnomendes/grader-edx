from Database import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, desc


Base = declarative_base()
class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    student_id = Column(String(50))
    problem_id = Column(String(50))
    program = Column(Text)
    test = Column(Text)


    def __init__(self, timestamp, student_id, problem_id, program, test):
        self.timestamp = timestamp
        self.student_id = student_id
        self.problem_id = problem_id
        self.program = program
        self.test = test


    @staticmethod
    def get_last_submissions_each_user(student_id, problem_id):
        session = Database.session()
        student_ids = [student_id[0] for student_id in set(session.query(Submission.student_id)) if not student_id[0] == student_id]

        submissions = [session.query(Submission).filter(Submission.student_id == student_id, Submission.problem_id == problem_id).order_by(desc(Submission.timestamp)).first() for student_id in student_ids]
        for s in submissions:
            session.expunge(s)
        session.close()
        return submissions

    @staticmethod
    def get_submission_user(student_id, problem_id):
        session = Database.session()
        s = session.query(Submission).filter(Submission.student_id == student_id, Submission.problem_id == problem_id).first()
        session.close()
        return s

session = Database.session(Base)
session.close()
