from Core.Executer import Executer
from Models.Submission import Submission


class TestExecuter():

    submission_program = Submission(None, "student_1234", "problem_1",
            "def sum(x, y):\n    return x + y", None, False)

    def test_pass_sample_code(self):
        submission_test = Submission(None, "student_567", "problem_1",
            None, "def test_sum():\n    assert sum(2, 2) == 4", False)

        test_result, fail_messages = Executer.run_test(self.submission_program, submission_test)
        assert test_result.coverage == 1
        assert test_result.errors == 0
        assert test_result.failures == 0
        assert test_result.tests == 1


    def test_fail_sample_code(self):
        submission_test = Submission(None, "student_567", "problem_1",
            None, "def test_sum():\n    assert sum(2, 2) == 5", False)

        test_result, fail_messages = Executer.run_test(self.submission_program, submission_test)
        assert test_result.coverage == 1
        assert test_result.errors == 0
        assert test_result.failures == 1
        assert test_result.tests == 1

    def test_error_sample_code(self):
        submission_test = Submission(None, "student_567", "problem_1",
            None, "def test_sum():\n    assert sum(2, 2) =* 5", False)

        test_result, fail_messages = Executer.run_test(self.submission_program, submission_test)
        assert test_result.errors == 1
        assert test_result.tests == 1
