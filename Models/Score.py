from Core.Database import Database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String


Base = declarative_base()


class Score(Base):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True)
    student_id = Column(String(50))
    score = Column(Float)

    def __init__(self, student_id, score):
        self.student_id = student_id
        self.score = score


session = Database.session(Base)
session.close()
