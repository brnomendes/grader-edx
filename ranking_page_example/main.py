import requests
from flask import Flask, render_template

app = Flask("ranking")
app.config["DEBUG"] = True


@app.route("/")
def index():
    scores = requests.get("http://localhost:1710/score").json()
    return render_template("index.html", scores=scores)


if __name__ == "__main__":
    app.run(port=9000)
