import time as t
import subprocess
import untangle
from Models.TestResult import TestResult
from Models.Submission import Submission
from Database import Database
from Scorer import Scorer
from Utils import Utils


class Grader():

    def __init__(self):
        self.session = Database.session()

    def run(self, submission):
        submissions = Submission.get_last_submissions_each_user(submission.student_id, submission.problem_id)
        for s in submissions:
            test_result = self.run_test(submission, s)
            sc = Scorer(submission.student_id, s.student_id, test_result)
            sc.start()
            if not s.id == submission.id:
                test_result = self.run_test(s, submission)
                sc = Scorer(s.student_id, submission.student_id, test_result)
                sc.start()
       

    def run_test(self, submission_program, submission_test):
        p_filename = "".join(["program", submission_program.student_id])
        Utils.write_to_file(p_filename, ".py", submission_program.program)

        t_filename = "".join(["test", submission_test.student_id])
        import_line = "".join(["from ", p_filename, " import *\n"])
        Utils.write_to_file(t_filename, ".py", "".join([import_line, submission_test.test]))

        p = subprocess.Popen(["pytest", t_filename + ".py", "-q", "--junitxml=result-" + submission_program.student_id + ".xml", "--cov=" + p_filename, "--cov-report=xml:cov-" + submission_program.student_id + ".xml"], stdout=subprocess.DEVNULL)
        p.wait()

        Utils.delete_file(p_filename, ".py")
        Utils.delete_file(t_filename, ".py")

        tests, errors, failures, time, coverage = self.xml_process(submission_program.student_id, submission_test.student_id)
        test_result = TestResult(submission_program.id, submission_test.id, tests, errors, failures, coverage, time)

        self.session.add(test_result)
        self.session.commit()
        return test_result


    def xml_process(self, student_id_program, student_id_test):
        x_filename = "".join(["result-", student_id_program])
        root = self.xml_parser(x_filename)

        tests = int(root.testsuite['tests'])
        errors = int(root.testsuite['errors'])
        failures = int(root.testsuite['failures'])
        time = float(root.testsuite['time'])
        coverage = 0

        if not errors:
            c_filename = "".join(["cov-", student_id_program])
            root = self.xml_parser(c_filename)
            coverage = float(root.coverage['line-rate'])

        return tests, errors, failures, time, coverage


    def xml_parser(self, filename):
        xml = open(filename + ".xml", "r")
        root = untangle.parse(xml.read())
        xml.close()
        Utils.delete_file(filename, ".xml")
        return root
