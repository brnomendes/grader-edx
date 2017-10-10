import os


class Utils():

    @staticmethod
    def write_to_file(filename, extension, content):
        file = open("".join([filename, extension]), 'w')
        file.write(content)
        file.close()

    @staticmethod
    def delete_file(filename, extension):
        os.remove("".join([filename, extension]))
