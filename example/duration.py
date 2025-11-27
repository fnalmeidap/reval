from reval import monitor
import time


@monitor.duration("example.compute")
def compute():
    time.sleep(0.02)


@monitor.duration("example.compute_heavy")
def compute_heavy():
    time.sleep(0.05)


while True:
    time.sleep(2)
    compute()
    compute_heavy()
