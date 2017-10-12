import datetime
from Models.Submission import Submission
from Core.Database import Database
from Core.Scorer import Scorer
from Core.Executer import Executer
from Core.Parser import Parser


class Grader():

    def __init__(self):
        self.session = Database.session()

    def run(self, anonymous_student_id, student_response, problem_id):
        submission = self._save_submission(anonymous_student_id, student_response, problem_id)
        if submission.error:
            return Grader._response(False)

        fail_messages = {}
        submissions = Submission.get_last_submissions_each_user(submission.problem_id)
        for s in submissions:
            messages = self._grader_execute(submission, s)
            if messages:
                fail_messages[s.student_id] = messages

            if not s.id == submission.id:
                self._grader_execute(s, submission)

        return Grader._response(fail_messages=fail_messages)

    def _grader_execute(self, submission_program, submission_test):
        test_result, fail_messages = Executer.run_test(submission_program, submission_test)
        self.session.add(test_result)
        self.session.commit()
        Scorer(submission_program.student_id, submission_test.student_id, test_result).start()
        return fail_messages

    def _save_submission(self, anonymous_student_id, student_response, problem_id):
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

    @staticmethod
    def _response(correct=True, fail_messages=None):
        if not correct:
            title = "<h3 style='color:red'><strong>Erro encontrado no Código.</strong></h3>"
            msg = "<p>Execute localmente em sua máquina os testes do seu programa antes de submetê-lo.</p>"
        else:
            title = "<h3><strong>Submissão aceita e pontuada.</strong></h3>"

            if fail_messages:
                if len(fail_messages) > 1:
                    msg = "<p>Os casos de testes de {} alunos encontraram falhas no seu programa.</p>".format(len(fail_messages))
                else:
                    msg = "<p>Os casos de testes de 1 aluno encontrou falhas no seu programa.</p>"
                fail_msg = "<pre style='color:red;'>{}</pre>".format(list(fail_messages.values())[0][0])
                msg = "{}<p><strong>Mensagem de falha:</strong></p>{}".format(msg, fail_msg)
            else:
                msg = "<p>Não foram encontradas falhas no seu programa por outros alunos.</p>"

        return {"correct": correct, "score": 1, "msg": "{}\n{}".format(title, msg)}
