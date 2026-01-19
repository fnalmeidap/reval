import reval
import time

reval.set_server_port(1234)

@reval.monitor("example.compute")
def compute_reval():
    reval.add_metadata({
        "task": "computation",
    })
    time.sleep(0.01)

def run_n_times(n: int, func: callable):
    for _ in range(n):
        func()

if __name__ == "__main__":
    while True:
        time.sleep(1)
        compute_reval()