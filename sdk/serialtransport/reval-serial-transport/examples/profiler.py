import psutil
import time

def cpu_watcher(interval=1.0):
    """
    Prints per-core and overall CPU usage.
    """
    # Warm-up
    psutil.cpu_percent(interval=None, percpu=True)

    while True:
        per_core = psutil.cpu_percent(interval=interval, percpu=True)
        overall = sum(per_core) / len(per_core)

        print(f"Overall CPU: {overall:.2f}%")
        for i, usage in enumerate(per_core):
            print(f"  Core {i}: {usage:.2f}%")
        print("-" * 30)

cpu_watcher()
