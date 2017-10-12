import subprocess
import untangle
from Models.TestResult import TestResult
from Core.Utils import Utils


class Executer:

    @staticmethod
    def run_test(s_program, s_test):
        p_filename = "program{}".format(s_program.student_id)
        Utils.write_to_file(p_filename, ".py", s_program.program)

        t_filename = "test{}".format(s_test.student_id)
        import_line = "from {} import *\n".format(p_filename)
        Utils.write_to_file(t_filename, ".py", "{}{}".format(import_line, s_test.test))

        p = subprocess.Popen(["pytest", "{}.py".format(t_filename), "-q",
            "--junitxml=result-{}.xml".format(s_program.student_id),
            "--cov={}".format(p_filename),
            "--cov-report=xml:cov-{}.xml".format(s_program.student_id)],
            stdout=subprocess.DEVNULL)

        p.wait()

        Utils.delete_file(p_filename, ".py")
        Utils.delete_file(t_filename, ".py")

        tests, errors, failures, time, coverage, fail_messages = Executer.xml_process(s_program.student_id, s_test.student_id)
        test_result = TestResult(s_program.id, s_test.id, tests, errors, failures, coverage, time)

        return test_result, fail_messages

    @staticmethod
    def xml_process(student_id_program, student_id_test):
        x_filename = "result-{}".format(student_id_program)
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

            c_filename = "cov-{}".format(student_id_program)
            root = Executer.xml_parser(c_filename)
            coverage = float(root.coverage['line-rate'])

        return tests, errors, failures, time, coverage, fail_messages

    @staticmethod
    def xml_parser(filename):
        xml = open("{}.xml".format(filename), "r")
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
