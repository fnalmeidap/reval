import time
import threading
import queue
import atexit

TO_MILLISECONDS = 1e-6
LOG_FILE = "experiment_b.log"
EXPERIMENT_NAME = "experiment_b"

# Queue for asynchronous logging
log_queue: queue.Queue[float] = queue.Queue()

def _log_writer():
    with open(LOG_FILE, "w") as f:
        while True:
            duration = log_queue.get()
            if duration is None:  # shutdown signal
                break
            f.write(f"{EXPERIMENT_NAME},{duration:.6f}\n")
            log_queue.task_done()

# Start background writer thread
_writer_thread = threading.Thread(target=_log_writer, daemon=True)
_writer_thread.start()

def shutdown_logger():
    log_queue.put(None)
    _writer_thread.join()

atexit.register(shutdown_logger)


def compute_reval():
    a = {}
    a["data"] = 10
    time.sleep(0.01)


def timed_call(func: callable):
    start_ns = time.perf_counter_ns()
    func()
    end_ns = time.perf_counter_ns()

    duration_ms = (end_ns - start_ns) * TO_MILLISECONDS
    log_queue.put(duration_ms)


def run_n_times(n: int, func: callable):
    for _ in range(n):
        timed_call(func)


if __name__ == "__main__":
    N = 1000

    start_ns = time.perf_counter_ns()
    run_n_times(N, compute_reval)
    end_ns = time.perf_counter_ns()

    total_duration_ms = (end_ns - start_ns) * TO_MILLISECONDS
    print(f"Total duration: {total_duration_ms:.3f} ms")

    # Ensure all measurements are written before exit
    log_queue.join()
