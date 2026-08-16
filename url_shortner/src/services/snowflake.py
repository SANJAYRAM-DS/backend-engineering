import time
import threading

# Custom Epoch (2024-01-01T00:00:00Z in ms)
EPOCH = 1704067200000

WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)
MAX_SEQUENCE = -1 ^ (-1 << SEQUENCE_BITS)

WORKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS


class SnowflakeIDGenerator:
    def __init__(self, worker_id: int = 1, datacenter_id: int = 1):
        if worker_id < 0 or worker_id > MAX_WORKER_ID:
            raise ValueError(f"worker_id must be between 0 and {MAX_WORKER_ID}")
        if datacenter_id < 0 or datacenter_id > MAX_DATACENTER_ID:
            raise ValueError(f"datacenter_id must be between 0 and {MAX_DATACENTER_ID}")

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = 0
        self.last_timestamp = -1
        self._lock = threading.Lock()

    def _time_gen(self) -> int:
        return int(time.time() * 1000)

    def generate_id(self) -> int:
        with self._lock:
            timestamp = self._time_gen()

            if timestamp < self.last_timestamp:
                # System clock moved backwards
                offset = self.last_timestamp - timestamp
                if offset <= 5:
                    time.sleep(offset / 1000.0)
                    timestamp = self._time_gen()
                else:
                    raise RuntimeError(f"Clock moved backwards. Refusing to generate ID for {offset}ms")

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & MAX_SEQUENCE
                if self.sequence == 0:
                    # Sequence exhausted in current millisecond, wait for next ms
                    while timestamp <= self.last_timestamp:
                        timestamp = self._time_gen()
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            snowflake_id = (
                ((timestamp - EPOCH) << TIMESTAMP_SHIFT)
                | (self.datacenter_id << DATACENTER_ID_SHIFT)
                | (self.worker_id << WORKER_ID_SHIFT)
                | self.sequence
            )
            return snowflake_id
