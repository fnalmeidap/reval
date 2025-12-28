import time

TO_MILLISECONDS = 1e-6

def compute_reval():
    a = {}
    a["data"] = 10
    time.sleep(0.2)

def run_n_times(n: int, func: callable):
    for _ in range(n):
        func()

if __name__ == "__main__":
    N = 100
    start_ns = time.perf_counter_ns()
    run_n_times(N, compute_reval)
    end_ns = time.perf_counter_ns()
    duration_ms = (end_ns - start_ns) * TO_MILLISECONDS

    print(duration_ms)