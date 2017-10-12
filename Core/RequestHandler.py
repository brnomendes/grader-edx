import json
from Core.Grader import Grader


class RequestHandler():

    @staticmethod
    def process_request(data):
        anonymous_student_id, student_response, problem_id = RequestHandler._process_raw_data(data)
        return Grader().run(anonymous_student_id, student_response, problem_id)

    @staticmethod
    def _process_raw_data(data):
        json_object = json.loads(data.decode("utf-8"))
        json_object = json.loads(json_object["xqueue_body"])

        student_response = json_object["student_response"]
        anonymous_student_id = json.loads(json_object["student_info"])["anonymous_student_id"]
        problem_id = json_object["grader_payload"]

        return anonymous_student_id, student_response, problem_id
