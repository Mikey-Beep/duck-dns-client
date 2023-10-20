import json
import requests
import yaml
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, Response
from pathlib import Path

config_path = Path(__file__).parent / "data" / "conf.yml"

app = Flask(__name__)


def send_req() -> str:
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
    )
    print(resp := str(response.content, encoding="utf-8"))
    return resp


@app.route("/update", methods=["GET"])
def update() -> Response:
    resp = {"duck_dns_response": send_req()}
    return Response(status=200, response=json.dumps(resp))


@app.route("/config", methods=["GET", "POST"])
def config() -> Response:
    if request.method == "GET":
        with config_path.open() as config_file:
            config_yaml = yaml.safe_load(config_file.read())
        return Response(status=200, response=json.dumps(config_yaml))
    elif request.method == "POST":
        with config_path.open("w") as config_file:
            config_file.write(yaml.safe_dump(request.json))
        resp = {"duck_dns_response": send_req()}
        return Response(status=200, response=json.dumps(resp))


with app.app_context():
    sched = BackgroundScheduler()
    sched.add_job(send_req, "interval", minutes=15)
    sched.start()

app.run(host="0.0.0.0", port=80)
