import pytest
import asyncio
from src.services.circuit_breaker import CircuitBreaker, CircuitBreakerOpenException


@pytest.mark.asyncio
async def test_circuit_breaker_closed_state():
    cb = CircuitBreaker(failure_threshold=3, recovery_time=1.0)

    async def dummy_func():
        return "ok"

    res = await cb.call(dummy_func)
    assert res == "ok"
    assert cb.state == "CLOSED"


@pytest.mark.asyncio
async def test_circuit_breaker_opens_on_failures():
    cb = CircuitBreaker(failure_threshold=3, recovery_time=1.0)

    async def failing_func():
        raise ValueError("error")

    for _ in range(3):
        with pytest.raises(ValueError):
            await cb.call(failing_func)

    assert cb.state == "OPEN"

    with pytest.raises(CircuitBreakerOpenException):
        await cb.call(failing_func)


@pytest.mark.asyncio
async def test_circuit_breaker_half_open_recovery():
    cb = CircuitBreaker(failure_threshold=2, recovery_time=0.2)

    async def failing_func():
        raise ValueError("error")

    for _ in range(2):
        with pytest.raises(ValueError):
            await cb.call(failing_func)

    assert cb.state == "OPEN"
    await asyncio.sleep(0.25)

    async def success_func():
        return "recovered"

    res = await cb.call(success_func)
    assert res == "recovered"
    assert cb.state == "CLOSED"
