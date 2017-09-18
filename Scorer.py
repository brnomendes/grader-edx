import threading
from Database import Database
from Models.Score import Score


class Scorer(threading.Thread):

    def __init__(self, student_id_program, student_id_test, test_result):
        threading.Thread.__init__(self)
        self.student_id_program = student_id_program
        self.student_id_test = student_id_test
        self.test_result = test_result
        self.session = Database.session()

    def run(self):
        s_program = self.get_score(self.student_id_program)
        s_test = self.get_score(self.student_id_test)

        if not self.test_result.errors:
            if not self.test_result.failures:
                self.increase_score(s_program, +10)
            else:
                for failure in range(self.test_result.failures):
                    if self.student_id_program == self.student_id_test:
                        self.increase_score(s_program, -50)
                    else:
                        self.increase_score(s_program, -2)

            self.increase_score(s_test, +10 * self.test_result.coverage)


    def get_score(self, student_id):
        s = self.session.query(Score).filter(Score.student_id == student_id).first()
        if not s:
            return self.create_new_score(student_id, 0)
        else:
            return s

    def create_new_score(self, student_id, score):
        s = Score(student_id, score)
        self.session.add(s)
        self.session.commit()
        return s

    def increase_score(self, s, increase):
        s.score = s.score + increase
        if s.score < 0:
            s.score = 0
        self.session.commit()

    @staticmethod
    def resubmission_score(student_id, increase):
        session = Database.session()
        s = session.query(Score).filter(Score.student_id == student_id).first()
        s.score = s.score + increase
        if s.score < 0:
            s.score = 0
        session.commit()
        session.close()