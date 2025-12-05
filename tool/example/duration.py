from reval import reval
from reval import settings
import time

settings.setup(host="127.0.0.1", port=7122)

@reval.monitor("example.compute")
def compute_reval():
    reval.add_metadata({
        "task": "computation_outside",
    })
    time.sleep(0.01)

@reval.monitor("example.compute_inner")
def run_n_times(n: int, func: callable):
    for _ in range(n):
        func()

if __name__ == "__main__":
    N = 10
    run_n_times(N, compute_reval)