import time
from collections import defaultdict, deque
from typing import Deque, Dict
from fastapi import Request, HTTPException


WINDOW_SECONDS = 60
MAX_REQUESTS = 120


class SlidingWindowLimiter:
    def __init__(self, window_seconds: int = WINDOW_SECONDS, max_requests: int = MAX_REQUESTS) -> None:
        self.window = window_seconds
        self.max_requests = max_requests
        self.bucket: Dict[str, Deque[float]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = time.time()
        q = self.bucket[key]
        # Evict old entries
        while q and now - q[0] > self.window:
            q.popleft()
        if len(q) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Too Many Requests")
        q.append(now)


limiter = SlidingWindowLimiter()


async def limit_requests(request: Request) -> None:
    # use client host as simple key; can combine with user/API key
    client = request.client.host if request.client else "unknown"
    limiter.check(client)


