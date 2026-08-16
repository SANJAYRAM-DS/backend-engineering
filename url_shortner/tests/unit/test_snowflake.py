import pytest
from src.services.snowflake import SnowflakeIDGenerator


def test_snowflake_uniqueness():
    gen = SnowflakeIDGenerator(worker_id=1, datacenter_id=1)
    ids = [gen.generate_id() for _ in range(1000)]
    assert len(ids) == len(set(ids)), "Generated IDs must be unique"


def test_snowflake_increasing():
    gen = SnowflakeIDGenerator(worker_id=1, datacenter_id=1)
    id1 = gen.generate_id()
    id2 = gen.generate_id()
    assert id2 > id1, "IDs generated subsequently must be monotonically increasing"


def test_snowflake_worker_id_validation():
    with pytest.raises(ValueError):
        SnowflakeIDGenerator(worker_id=999, datacenter_id=1)
