import subprocess
import untangle
from Models.TestResult import TestResult
from Core.Utils import Utils


class Executer:

    @staticmethod
    def run_test(submission_program, submission_test):
        p_filename = "".join(["program", submission_program.student_id])
        Utils.write_to_file(p_filename, ".py", submission_program.program)

        t_filename = "".join(["test", submission_test.student_id])
        import_line = "".join(["from ", p_filename, " import *\n"])
        Utils.write_to_file(t_filename, ".py", "".join([import_line, submission_test.test]))

        p = subprocess.Popen(["pytest", t_filename + ".py", "-q", "--junitxml=result-" + submission_program.student_id + ".xml", "--cov=" + p_filename, "--cov-report=xml:cov-" + submission_program.student_id + ".xml"], stdout=subprocess.DEVNULL)
        p.wait()

        Utils.delete_file(p_filename, ".py")
        Utils.delete_file(t_filename, ".py")

        tests, errors, failures, time, coverage, fail_messages = Executer.xml_process(submission_program.student_id, submission_test.student_id)
        test_result = TestResult(submission_program.id, submission_test.id, tests, errors, failures, coverage, time)

        return test_result, fail_messages

    @staticmethod
    def xml_process(student_id_program, student_id_test):
        x_filename = "".join(["result-", student_id_program])
        root = Executer.xml_parser(x_filename)

        tests = int(root.testsuite['tests'])
        errors = int(root.testsuite['errors'])
        failures = int(root.testsuite['failures'])
        time = float(root.testsuite['time'])
        fail_messages = None
        coverage = 0

        if not errors:
            if failures:
                fail_messages = Executer.get_fail_messages(root)

            c_filename = "".join(["cov-", student_id_program])
            root = Executer.xml_parser(c_filename)
            coverage = float(root.coverage['line-rate'])

        return tests, errors, failures, time, coverage, fail_messages

    @staticmethod
    def xml_parser(filename):
        xml = open(filename + ".xml", "r")
        root = untangle.parse(xml.read())
        xml.close()
        Utils.delete_file(filename, ".xml")
        return root


    @staticmethod
    def get_fail_messages(untangle_root):
        msgs = []
        for test in untangle_root.testsuite.children:
            if test.get_elements('failure'):
                msg = test.get_elements('failure')[0].cdata
                msgs.append(msg.replace(msg.split('\n')[-1], ""))
        return msgs
