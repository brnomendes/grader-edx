import json
import datetime
from Models.Submission import Submission
from Database import Database
from Scorer import Scorer
from Grader import Grader
from Parser import Parser


class RequestHandler():

    @staticmethod
    def process(data):
        anonymous_student_id, student_response = RequestHandler.process_data(data)
        submission = RequestHandler.save_submission(anonymous_student_id, student_response)
        Grader().run(submission)
        return RequestHandler.response()


    @staticmethod
    def process_data(data):
        json_object = json.loads(data.decode("utf-8"))
        json_object = json.loads(json_object["xqueue_body"])

        student_response = json_object["student_response"]
        anonymous_student_id = json.loads(json_object["student_info"])["anonymous_student_id"]

        return anonymous_student_id, student_response


    @staticmethod
    def save_submission(anonymous_student_id, student_response):
        session = Database.session()
        program, test = Parser.parse(student_response)
        new_submission = Submission(datetime.datetime.now(), anonymous_student_id, program, test)
        if Submission.get_submission_user(new_submission.student_id):
            Scorer.resubmission_score(new_submission.student_id, -100)
        session.add(new_submission)
        session.commit()
        session.expunge(new_submission)
        session.close()
        return new_submission


    @staticmethod
    def response():
        return {"correct": True, "score": 0, "msg": "Submissão Recebida"}
