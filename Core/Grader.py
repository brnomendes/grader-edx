from Models.Submission import Submission
from Core.Scorer import Scorer
from Core.Executer import Executer
from Core.Database import Database


class Grader():

    def __init__(self):
        self.session = Database.session()

    def run(self, submission):
        submissions = Submission.get_last_submissions_each_user(submission.student_id, submission.problem_id)
        for s in submissions:
            test_result = Executer.run_test(submission, s)
            sc = Scorer(submission.student_id, s.student_id, test_result)
            sc.start()
            if not s.id == submission.id:
                test_result = Executer.run_test(s, submission)
                self.session.add(test_result)
                self.session.commit()
                sc = Scorer(s.student_id, submission.student_id, test_result)
                sc.start()
