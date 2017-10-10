from Models.Submission import Submission
from Core.Database import Database
from Core.Scorer import Score
from sqlalchemy import func, desc


class Ranking():

    @staticmethod
    def get_all():
        session = Database.session()
        scores = session.query(Score).order_by(desc(Score.score)).all()

        return [{"student_id": s.student_id,
                "submissions": session.query(func.count(Submission.id))
                .filter(Submission.student_id == s.student_id).scalar(),
                "score": s.score}
                for s in scores]
