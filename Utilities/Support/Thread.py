import threading
import queue
import functools
import time
from collections import deque
import cv2

class BoundedBuffer:

    def __init__(self, maxlen=128, lifo=False):
        if maxlen <= 0:
            raise ValueError("buffer_size must be > 0")
        self._dq = deque(maxlen=maxlen)
        self._lock = threading.Lock()
        self._lifo = lifo

    def put(self, item):
        with self._lock:
            self._dq.append(item)

    def empty(self):
        with self._lock:
            return len(self._dq) == 0

    def get_nowait(self):
        with self._lock:
            if not self._dq:
                raise queue.Empty
            return self._dq.pop() if self._lifo else self._dq.popleft()

    def get(self):
        return self.get_nowait()

    def drain(self):
        with self._lock:
            items = list(self._dq)
            self._dq.clear()
            return items

class ThreadManager:
    def __init__(self, tasks=None, keep_timestamp=False, lifo=True, buffer_size=128):
        self.queues = {}
        self.latest_results = {}
        self.runs = {}
        self.threads = []
        self.running = True
        self.keep_timestamp = keep_timestamp
        self.lifo = lifo
        self.default_buffer_size = buffer_size
        tasks = tasks or []
        for task in tasks:
            # Allow tuple like (func, *args) or dict with options
            if isinstance(task, dict):
                self.register_task(**task)
            else:
                self.register_task(*task)

    def keep_timestamps(self, keep_timestamp):
        self.keep_timestamp = keep_timestamp

    def _run_task(self, name, task):
        while self.running:
            result = task()
            self.runs[name] += 1
            if result is not None:
                # Non-blocking put; buffer drops oldest if full
                result = {"fresh": True, "result": result}
                if self.keep_timestamp:
                    result["time"] = time.time()
                self.queues[name].put(result)

    def register_task(self, func, *args, buffer_size=None, **kwargs):
        name = func.__name__
        bsize = buffer_size if buffer_size is not None else self.default_buffer_size
        self.queues[name] = BoundedBuffer(maxlen=bsize, lifo=self.lifo)
        self.latest_results[name] = {"fresh": False, "result": None}
        if self.keep_timestamp:
            self.latest_results[name]["time"] = time.time()
        self.runs[name] = 0

        task = functools.partial(func, *args, **kwargs)
        thread = threading.Thread(target=self._run_task, args=(name, task), daemon=True)
        self.threads.append(thread)

    def print_registered_functions(self):
        print("Registered functions:")
        for name in self.queues:
            print(f" - {name}")
        print()

    def all(self, func):
        name = func.__name__
        if name not in self.queues:
            raise Exception(f"Function {name} is not registered. Use print_registered_functions().")
        return self.queues[name].drain()

    def latest(self, func):
        name = func.__name__
        if name not in self.queues:
            raise Exception(f"Function {name} is not registered. Use print_registered_functions().")
        try:
            result = self.queues[name].get_nowait()
            self.latest_results[name] = result
            return result
        except queue.Empty:
            result = self.latest_results[name]
            result["fresh"] = False
            return result

    def get_number_of_runs(self, func):
        name = func.__name__
        if name not in self.queues:
            raise Exception(f"Function {name} is not registered.")
        return self.runs[name]

    def start(self):
        for thread in self.threads:
            thread.start()

    def stop(self):
        self.running = False
        for thread in self.threads:
            thread.join(timeout=1.0)


# --- Main program (GUI stays here) ---

if __name__ == "__main__":

    def fast_function():
        time.sleep(0.6)
        return "."

    def slow_function():
        time.sleep(5)
        return 3*"-"

    cap = cv2.VideoCapture(0)

    manager = ThreadManager()

    manager.register_task(fast_function)
    manager.register_task(slow_function)

    manager.start()

    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
    fast_total = ""
    slow_total = ""
    while True:

        ok, frame = cap.read()
        frame_t = time.time()

        # fast results
        fast_latest = manager.latest(fast_function)
        if fast_latest["fresh"]:
            fast_total += fast_latest["result"]

        # slow results
        slow_latest = manager.latest(slow_function)
        if slow_latest["fresh"]:
            slow_total += slow_latest["result"]

        # let's check the results

        if fast_latest is not None:
            cv2.putText(frame, "Fast", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(frame, fast_total, (100, 45),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)

        if slow_latest is not None:
            cv2.putText(frame, "Slow", (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            cv2.putText(frame, slow_total, (100, 108),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)

        # thanks to our main thread we can always print the frame!
        if frame is not None:
            cv2.imshow("Live", frame)

        if (cv2.waitKey(1) & 0xFF) == 27:
            break


    manager.stop()
    cap.release()
    cv2.destroyAllWindows()