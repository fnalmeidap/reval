from datetime import datetime
import json
import random
import time
from elasticsearch import Elasticsearch

# Connect to Elasticsearch (default localhost:9200)
es = Elasticsearch("http://localhost:9200")

# Define the index name
index_name = "logs"


doc = {}
doc["timestamp"] = datetime.utcnow().isoformat()
doc["level"] = "INFO"
doc["service"] = "my-service"
doc["message"] = "This is a test log message"

# Index the document into Elasticsearch

import json
from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch("http://localhost:9200")

total_bytes_sent = 0
total_docs_sent = 0

def send_log(doc, index_name="app-logs"):
    global total_bytes_sent, total_docs_sent

    # Serialize exactly once to measure size
    payload = json.dumps(doc, separators=(",", ":"), ensure_ascii=False)
    payload_size = len(payload.encode("utf-8"))

    print(f"Payload size: {payload_size} bytes")
    print(f"Object size in bytes: {doc.__sizeof__()} bytes")

    # Update counters
    total_bytes_sent += payload_size
    total_docs_sent += 1

    # Send as dict (NOT as string)
    res = es.index(index=index_name, document=doc)

    return payload_size, res["result"]


while True:
    time.sleep(0.2)
    seed = random.randint(1, 100)
    doc["message"] = f"This is a test log message with random number {seed}"

    if seed > 50:
        doc["service"] = "other-service"
    else:
        doc["service"] = "my-service"

    doc["timestamp"] = datetime.utcnow().isoformat()
    size, result = send_log(doc)

    print(f"Sent {size} bytes | total={total_bytes_sent} bytes | result={result}")
