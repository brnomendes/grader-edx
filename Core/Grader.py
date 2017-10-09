import datetime
from Models.Submission import Submission
from Core.Database import Database
from Core.Scorer import Scorer
from Core.Executer import Executer
from Core.Parser import Parser


class Grader():

    def __init__(self):
        self.session = Database.session()
        self.fail_messages = {}

    def run(self, anonymous_student_id, student_response, problem_id):
        submission = self.save_submission(anonymous_student_id, student_response, problem_id)
        if submission.error:
            return False, "Erro Encontrado no Código"

        submissions = Submission.get_last_submissions_each_user(submission.problem_id)
        for s in submissions:
            messages = self.grader_execute(submission, s)
            if messages:
                self.fail_messages[s.student_id] = messages

            if not s.id == submission.id:
                self.grader_execute(s, submission)

        return True, "Submissão Aceita"

    def grader_execute(self, submission_program, submission_test):
        test_result, fail_messages = Executer.run_test(submission_program, submission_test)
        self.session.add(test_result)
        self.session.commit()
        sc = Scorer(submission_program.student_id, submission_test.student_id, test_result)
        sc.start()
        return fail_messages


    def save_submission(self, anonymous_student_id, student_response, problem_id):
        program, test = Parser.parse(student_response)
        new_submission = Submission(datetime.datetime.now(), anonymous_student_id, problem_id, program, test, False)
        test_result, fail_messages = Executer.run_test(new_submission, new_submission)
        new_submission.error = True if test_result.errors > 0 else False

        submission_exists = Submission.get_submission_user(new_submission.student_id, problem_id)
        if submission_exists:
            Scorer.resubmission_score(new_submission.student_id, -100)

        Scorer(None, None, None).get_score(new_submission.student_id)

        self.session.add(new_submission)
        self.session.commit()
        self.session.expunge(new_submission)
        self.session.close()

        return new_submission
