from reval import reval
import time


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
    N = 1000
    run_n_times(N, compute_reval)