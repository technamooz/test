import time
from collections import defaultdict


class SlidingWindow:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window_seconds = window_seconds
        self.events: defaultdict[str, list[float]] = defaultdict(list)

    def allowed(self, key: str) -> bool:
        now = time.monotonic()
        recent = [item for item in self.events[key] if now - item < self.window_seconds]
        self.events[key] = recent
        if len(recent) >= self.limit:
            return False
        recent.append(now)
        return True


login_limiter = SlidingWindow(limit=8, window_seconds=300)
