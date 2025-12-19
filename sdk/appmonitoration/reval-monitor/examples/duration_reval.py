import time
from reval.monitor import reval

reval.set_server_port(1234)

@reval.monitor("example.compute")
def compute_reval():
    reval.add_metadata({
        "task": "computation_outside",
    })

@reval.monitor("example.compute_inner")
def run_n_times(n: int, func: callable):
    for _ in range(n):
        func()

if __name__ == "__main__":
    N = 100
    run_n_times(N, compute_reval)