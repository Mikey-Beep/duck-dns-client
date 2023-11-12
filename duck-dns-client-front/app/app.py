"""This module handles the UI for configuring the DuckDNS client.
"""
import json
import requests
from flask import Flask, render_template, request, Response

app = Flask(__name__)


@app.route("/")
def index():
    """Serves the homepage.
    """
    return render_template("index.html")


@app.route("/update", methods=["GET"])
def update() -> Response:
    """Proxies the DuckDNS update functionality.
    """
    url = "http://back/update"
    response = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(response.json()))


@app.route("/config", methods=["GET", "POST"])
def config() -> Response:
    """Proxies the config functionality.
    """
    url = "http://back/config"
    if request.method == "POST":
        response = requests.post(url, json=request.json, timeout=10)
        return Response(status=200, response=json.dumps(response.json()))
    response = requests.get(url, timeout=10)
    return Response(status=200, response=json.dumps(response.json()))


app.run(host="0.0.0.0", port=80)
