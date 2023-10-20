import json
import requests
from flask import Flask, render_template, request, Response

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/update", methods=["GET"])
def update() -> Response:
    url = f"http://back/update"
    response = requests.get(url)
    return Response(status=200, response=json.dumps(response.json()))


@app.route("/config", methods=["GET", "POST"])
def config() -> Response:
    url = f"http://back/config"
    if request.method == "GET":
        response = requests.get(url)
        return Response(status=200, response=json.dumps(response.json()))
    elif request.method == "POST":
        response = requests.post(url, json=request.json)
        return Response(status=200, response=json.dumps(response.json()))


app.run(host="0.0.0.0", port=80)
