from reval import reval
import time


@reval.monitor("example.compute")
def compute():
    reval.add_metadata({"task": "computelol"})
    time.sleep(0.02)


@reval.monitor("example.compute_heavy")
def compute_heavy():
    time.sleep(0.05)


while True:
    time.sleep(2)
    compute()
    compute_heavy()
