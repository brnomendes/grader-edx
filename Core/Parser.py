class Parser():

    @staticmethod
    def parse(student_response):
        program = ""
        test = ""
        lines = student_response.splitlines(True)

        in_test = False
        for line in lines:
            if line.startswith("def test_"):
                in_test = True
            elif in_test and not line.startswith((" ", "\t")):
                in_test = False

            if in_test:
                test = test + line
            else:
                program = program + line

        return program, test
