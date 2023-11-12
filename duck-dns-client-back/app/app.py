"""This module handles the background tasks to keep the DuckDNS record updated.
"""
import json
from pathlib import Path
import requests
import yaml
from flask import Flask, request, Response
from apscheduler.schedulers.background import BackgroundScheduler

config_path = Path(__file__).parent / "data" / "conf.yml"

app = Flask(__name__)


def send_req() -> str:
    """Sends the update request to DuckDNS
    """
    with config_path.open() as config_file:
        config_yaml = yaml.safe_load(config_file.read())
    response = requests.get(
        "https://www.duckdns.org/update",
        params={
            "domains": config_yaml["domain"],
            "token": config_yaml["token"],
            "ip": "",
            "verbose": "true",
        },
        timeout=10
    )
    print(resp := str(response.content, encoding="utf-8"))
    return resp


@app.route("/update", methods=["GET"])
def update() -> Response:
    """Endpoint to force update of the DuckDNS record.
    """
    resp = {"duck_dns_response": send_req()}
    return Response(status=200, response=json.dumps(resp))


@app.route("/config", methods=["GET", "POST"])
def config() -> Response:
    """Endpoint to handle fetching and updating the DuckDNS config.
    """
    if request.method == "POST":
        with config_path.open("w") as config_file:
            config_file.write(yaml.safe_dump(request.json))
        resp = {"duck_dns_response": send_req()}
        return Response(status=200, response=json.dumps(resp))
    with config_path.open() as config_file:
        config_yaml = yaml.safe_load(config_file.read())
    return Response(status=200, response=json.dumps(config_yaml))


with app.app_context():
    sched = BackgroundScheduler()
    sched.add_job(send_req, "interval", minutes=15)
    sched.start()

app.run(host="0.0.0.0", port=80)
