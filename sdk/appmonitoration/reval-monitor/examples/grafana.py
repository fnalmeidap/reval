import time
import json
import requests
import random

LOKI_URL = "http://localhost:3100/loki/api/v1/push"

def send_log(message: str, labels: dict):
    payload = {
        "streams": [
            {
                "stream": labels,
                "values": [
                    [
                        str(int(time.time() * 1_000_000_000)),  # ns timestamp
                        message
                    ]
                ]
            }
        ]
    }

    response = requests.post(
        LOKI_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=2
    )

    response.raise_for_status()

if __name__ == "__main__":
    while True:
        time.sleep(0.1)
        send_log(
            message=json.dumps({
                "event": "robot_started",
                "mode": "autonomous",
                "duration": f"{random.randint(1, 100)%10}"
            }),
            labels={
                "service": "controller",
                "level": "info"
            }
        )

        print("Log sent successfully")
