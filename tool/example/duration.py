from reval import reval
import time


@reval.monitor("example.compute")
def compute():
    reval.add_metadata({"task": "computelol", "priority": "high", "driele": "linda"})
    time.sleep(0.02)


while True:
    time.sleep(2)
    compute()
