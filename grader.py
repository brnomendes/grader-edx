import os
import json
import datetime
import subprocess
import untangle
from submission import Submission

class Grader():

    def __init__(self):
        pass


    def run(self, body_content):
        student_response, anonymous_student_id = self._get_data(body_content)
        return self._grade(student_response, anonymous_student_id)


    def _get_data(self, body_content):
        json_object = json.loads(body_content)
        json_object = json.loads(json_object["xqueue_body"])

        student_response = json_object["student_response"]
        anonymous_student_id = json.loads(json_object["student_info"])["anonymous_student_id"]

        return student_response, anonymous_student_id


    def _grade(self, student_response, anonymous_student_id):
        program, test = Submission.parser(student_response)
        submission = Submission(datetime.datetime.now(), anonymous_student_id, program, test)
        submission.save()

        program_name = "program" + anonymous_student_id
        program_file = open(program_name + ".py", 'w')
        program_file.write(program)
        program_file.close()

        submissions = Submission.get_all()
        for s in submissions:
            test_name = "test" + s.student_id
            test_file = open(test_name + ".py", 'w')
            test_file.write("from " + program_name + " import *\n" + s.test)
            test_file.close()
            p = subprocess.Popen(["pytest", test_name + ".py", "-q", "--junitxml=result-" + submission.student_id + ".xml", "--cov=" + program_name, "--cov-report=xml:cov-" + submission.student_id + ".xml"], stdout=subprocess.DEVNULL)
            p.wait()
            tests, errors, failures, time, coverage = self._xml_process(submission.student_id, s.student_id)
            Submission.save_test_results(submission.id, s.student_id, tests, errors, failures, coverage, time)
            os.remove(test_name + ".py")

        os.remove(program_name + ".py")

        return self._process_result()


    def _process_result(self):
        # TODO
        result = {}
        result.update({"correct": True, "score": 0, "msg": "Ok!"})
        result = json.dumps(result)
        return result.encode('utf-8')


    def _xml_process(self, student_id_program, student_id_test):
        xml_result = open("result-" + student_id_program + ".xml", "r")
        root = untangle.parse(xml_result.read())
        tests = int(root.testsuite['tests'])
        errors = int(root.testsuite['errors'])
        failures = int(root.testsuite['failures'])
        time = float(root.testsuite['time'])
        coverage = 0
        xml_result.close()
        os.remove("result-" + student_id_program + ".xml")

        if not errors:
            #if failures:
            #    fail_messages = {}
            #    for test in root.testsuite.children:
            #        if test.get_elements('failure'):
            #            name = test.get_attribute('name')
            #            failure = test.get_elements('failure')
            #            fail_messages[name] = failure[0]['message']

            xml_coverage = open("cov-" + student_id_program + ".xml", "r")
            root = untangle.parse(xml_coverage.read())
            coverage = float(root.coverage['line-rate'])
            xml_coverage.close()
            os.remove("cov-" + student_id_program + ".xml")

        return tests, errors, failures, time, coverage
