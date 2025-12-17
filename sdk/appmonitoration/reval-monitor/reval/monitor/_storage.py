import requests
import json
from datetime import datetime, timezone
import random

INFLUX_URL = "http://localhost:8086"
TOKEN = "mytoken"      # <-- Your token goes here
ORG = "myorg"
BUCKET = "reval"

def write_json(json_obj):
    # Convert dict → json string
    json_string = json.dumps(json_obj)

    # Escape quotes for line protocol
    json_string = json_string.replace('"', '\\"')

    # Build line protocol
    # measurement field="json string"
    line = f'json_events value="{json_string}"'

    response = requests.post(
        f"{INFLUX_URL}/api/v2/write?org={ORG}&bucket={BUCKET}&precision=ns",
        data=line,
        headers={
            "Authorization": f"Token {TOKEN}",   # <-- TOKEN GOES HERE
            "Content-Type": "text/plain; charset=utf-8",
        }
    )

    if response.status_code not in (204, 200):
        print("Error:", response.status_code, response.text)
    else:
        print("Write OK")

# Example usage
while True:
    write_json({
        "value": random.randint(1, 100)
    })