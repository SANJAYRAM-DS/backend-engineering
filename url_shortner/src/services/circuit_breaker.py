import time
import asyncio
from typing import Callable, Any


class CircuitBreakerOpenException(Exception):
    """Raised when request is rejected because Circuit Breaker is OPEN."""
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_time: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_state_change = time.time()
        self._lock = asyncio.Lock()

    async def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        async with self._lock:
            now = time.time()
            if self.state == "OPEN":
                if now - self.last_state_change > self.recovery_time:
                    self.state = "HALF-OPEN"
                    self.last_state_change = now
                else:
                    raise CircuitBreakerOpenException("Circuit breaker is OPEN. Fast failing call.")

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            async with self._lock:
                if self.state == "HALF-OPEN":
                    self.state = "CLOSED"
                    self.failure_count = 0
                    self.last_state_change = time.time()
                elif self.state == "CLOSED":
                    self.failure_count = 0

            return result
        except Exception as e:
            async with self._lock:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    self.last_state_change = time.time()
            raise e
