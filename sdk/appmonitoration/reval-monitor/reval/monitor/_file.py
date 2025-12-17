from pathlib import Path
import atexit

LOG_PATH = Path("/home/fnap/workspace/tools/reval/experiment_nested").with_suffix(".log")
print(f"Logging to {LOG_PATH}")
LOG_FILE = open(LOG_PATH, "a", encoding="utf-8", buffering=1)  # line-buffered

def _close_log():
    try:
        LOG_FILE.close()
    except Exception:
        pass

atexit.register(_close_log)

def _write_log(line: str):
    LOG_FILE.write(line + "\n")