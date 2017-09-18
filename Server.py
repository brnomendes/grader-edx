from RequestHandler import RequestHandler
from flask import Flask, request

app = Flask("external-grader")
app.config["DEBUG"] = True

@app.route("/", methods=["POST"])
def post():
    return RequestHandler.process(request.data)

if __name__ == "__main__":
    app.run()