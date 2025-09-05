import threading
import time
from queue import Queue


def timed_input(prompt: str, timeout: int = 15) -> str | None:
    """
    Input function with countdown timer.
    Returns None if time runs out.
    """
    q = Queue()
    stop = threading.Event()

    def reader():
        try:
            s = input(prompt)
            if not stop.is_set():
                q.put(s)
        except EOFError:
            pass

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    for remaining in range(timeout, 0, -1):
        print(f"\r⏳ {remaining:2d}s left, please enter…", end="", flush=True)
        time.sleep(1)
        if not q.empty():
            print("\r" + " " * 40 + "\r", end="")
            stop.set()
            return q.get()

    stop.set()
    print("\r" + " " * 40 + "\r", end="")
    return None
