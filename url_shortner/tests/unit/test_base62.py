import pytest
from src.services.base62 import encode_base62, decode_base62


def test_base62_encoding_decoding():
    test_numbers = [0, 1, 61, 62, 125, 999999, 123456789012345]
    for num in test_numbers:
        encoded = encode_base62(num)
        assert isinstance(encoded, str)
        decoded = decode_base62(encoded)
        assert decoded == num


def test_base62_zero():
    assert encode_base62(0) == "0"
    assert decode_base62("0") == 0


def test_base62_invalid_char():
    with pytest.raises(ValueError):
        decode_base62("abc@123")