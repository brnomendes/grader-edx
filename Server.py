from Core.RequestHandler import RequestHandler
from flask import Flask, request, jsonify
from Models.Score import Score

app = Flask("external-grader")
app.config["DEBUG"] = True


@app.route("/", methods=["POST"])
def post():
    return jsonify(RequestHandler.process(request.data))


@app.route("/score", methods=["GET"])
def get_score():
    return jsonify([{"student_id": s.student_id, "score": s.score} for s in Score.get_all()])


if __name__ == "__main__":
    app.run(port=1710)
