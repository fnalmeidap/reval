import time
import threading
import queue
import atexit
import psutil

LOG_FILE = "memory_experiment_e.log"
SAMPLE_INTERVAL_SEC = 0.005  # 5 ms

log_queue: queue.Queue[tuple[float, float]] = queue.Queue()
stop_event = threading.Event()


def _file_writer():
    with open(LOG_FILE, "w") as f:
        while True:
            item = log_queue.get()
            if item is None:
                break

            timestamp_sec, memory_mb = item
            f.write(f"{timestamp_sec:.6f},{memory_mb:.3f}\n")
            log_queue.task_done()


def _memory_sampler():
    process = psutil.Process()
    start_time = time.perf_counter()

    while not stop_event.is_set():
        elapsed = time.perf_counter() - start_time
        rss_mb = process.memory_info().rss / (1024 * 1024)

        log_queue.put((elapsed, rss_mb))
        time.sleep(SAMPLE_INTERVAL_SEC)


_writer_thread = threading.Thread(target=_file_writer, daemon=True)
_sampler_thread = threading.Thread(target=_memory_sampler, daemon=True)

_writer_thread.start()
_sampler_thread.start()


def shutdown():
    stop_event.set()
    _sampler_thread.join()
    log_queue.put(None)
    _writer_thread.join()


atexit.register(shutdown)


# ------------------ Example workload ------------------

def compute():
    data = {}
    data["test"] = "x"
    time.sleep(0.01)


def run_n_times(n, func):
    for _ in range(n):
        func()


if __name__ == "__main__":
    run_n_times(1000, compute)

    # Ensure all samples are flushed
    log_queue.join()
