import threading
from Core.Database import Database
from Models.Score import Score


class Scorer(threading.Thread):

    def __init__(self, student_id_program, student_id_test, test_result):
        threading.Thread.__init__(self)
        self._student_id_program = student_id_program
        self._student_id_test = student_id_test
        self._test_result = test_result
        self._session = Database.session()

    def run(self):
        s_program = self.get_score(self._student_id_program)
        s_test = self.get_score(self._student_id_test)

        if not self._test_result.errors:
            if self._student_id_program == self._student_id_test:
                for failure in range(self._test_result.failures):
                    self._increase_score(s_program, -50)
                self._session.close()
                return

            if not self._test_result.failures:
                self._increase_score(s_program, +10)
            else:
                for failure in range(self._test_result.failures):
                    self._increase_score(s_test, +2)
                    self._increase_score(s_program, -2)
            self._increase_score(s_test, +10 * self._test_result.coverage)
        self._session.close()

    def _increase_score(self, s, increase):
        s.score = s.score + increase
        self._session.commit()

    def get_score(self, student_id):
        s = self._session.query(Score).filter(Score.student_id == student_id).first()
        if not s:
            return self._create_new_score(student_id, 0)
        else:
            return s

    def _create_new_score(self, student_id, score):
        s = Score(student_id, score)
        self._session.add(s)
        self._session.commit()
        return s

    @staticmethod
    def resubmission_score(student_id, increase):
        session = Database.session()
        s = session.query(Score).filter(Score.student_id == student_id).first()
        s.score = s.score + increase
        session.commit()
        session.close()
