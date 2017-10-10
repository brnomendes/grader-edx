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
            return self.response(False)

        submissions = Submission.get_last_submissions_each_user(submission.problem_id)
        for s in submissions:
            messages = self.grader_execute(submission, s)
            if messages:
                self.fail_messages[s.student_id] = messages

            if not s.id == submission.id:
                self.grader_execute(s, submission)

        return self.response()

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


    def response(self, correct=True):
        if not correct:
            title = "<h3 style='color:red'><strong>Erro Encontrado no Código.</strong></h3>"
            msg = "<p>Execute localmente em sua máquina os testes do seu programa antes de submetê-lo.</p>"
            return False, "\n".join([title, msg])

        title = "<h3><strong>Submissão Aceita e Pontuada.</strong></h3>"
        if self.fail_messages:
            if len(self.fail_messages) > 1:
                msg = "<p>Os casos de testes de {} alunos encontraram falhas no seu programa.</p>\n".format(len(self.fail_messages))
            else:
                msg = "<p>Os casos de testes de 1 aluno encontrou falhas no seu programa.</p>\n"

            fail_msg = "<p style='color:red;'>{}</p>".format(list(self.fail_messages.values())[0][0])
            msg = "".join([msg, "<p><strong>Mensagem de falha:</strong></p>", fail_msg])
        else:
            msg = "<p>Não foram encontradas falhas no seu programa por outros alunos.</p>"
        return True, "\n".join([title, msg])
