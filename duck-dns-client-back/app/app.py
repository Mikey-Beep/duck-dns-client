import requests
import yaml
from apscheduler.schedulers.blocking import BlockingScheduler
from pathlib import Path

config_path = Path(__file__).parent / "data" / "conf.yml"

sched = BlockingScheduler()


@sched.scheduled_job("interval", seconds=10)
def send_req():
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
    print(str(response.content, encoding="utf-8"))


sched.start()
