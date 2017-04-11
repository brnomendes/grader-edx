import pymysql


class Submission():

    def __init__(self, timestamp, student_id, program, test):
        self.timestamp = timestamp
        self.student_id = student_id
        self.program = program
        self.test = test
        self.id = None


    def save(self):
        db = pymysql.connect("localhost", "root", "root", "grader")
        cursor = db.cursor()

        sql = "INSERT INTO Submissions(timestamp, student_id, program, test) VALUES ('%s', '%s', '%s', '%s')" % (self.timestamp, self.student_id, self.program, self.test)
        try:
            cursor.execute(sql)
            db.commit()
            self.id = cursor.lastrowid
        except pymysql.MySQLError as error:
            print(error.args)
            db.rollback()
        db.close()


    @staticmethod
    def get_all():
        db = pymysql.connect("localhost", "root", "root", "grader")
        cursor = db.cursor()
        results = []

        try:
            cursor.execute("SELECT student_id FROM Submissions")
            student_ids = list(set(cursor.fetchall()))

            for student_id in student_ids:
                sql = "SELECT * FROM Submissions WHERE student_id = '%s' ORDER BY timestamp DESC LIMIT 1" % student_id[0]
                cursor.execute(sql)
                result = cursor.fetchall()
                result = result[0]
                s = Submission(result[1], result[2], result[3], result[4])
                results.append(s)
        except pymysql.MySQLError as error:
            print(error.args)

        db.close()
        return results


    @staticmethod
    def parser(student_response):
        program = ""
        test = ""
        lines = student_response.splitlines(True)

        in_test = False
        for line in lines:
            if line.startswith("def test_"):
                in_test = True

            if in_test:
                test = test + line
            else:
                program = program + line

        return program, test


    @staticmethod
    def save_test_results(submission_id, student_id_test, tests, errors, failures, coverage, time):
        db = pymysql.connect("localhost", "root", "root", "grader")
        cursor = db.cursor()

        sql = "INSERT INTO TestResults(submission_id, student_id_test, tests, errors, failures, coverage, time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (submission_id, student_id_test, tests, errors, failures, coverage, time)
        try:
            cursor.execute(sql)
            db.commit()
        except pymysql.MySQLError as error:
            print(error.args)
            db.rollback()
        db.close()
