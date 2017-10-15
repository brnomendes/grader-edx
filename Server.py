from Core.RequestHandler import RequestHandler
from flask import Flask, request, jsonify
from Core.Ranking import Ranking

app = Flask("external-grader")


@app.route("/", methods=["POST"])
def post():
    return jsonify(RequestHandler.process_request(request.data))


@app.route("/score", methods=["GET"])
def get_score():
    return jsonify(Ranking.get_all())
