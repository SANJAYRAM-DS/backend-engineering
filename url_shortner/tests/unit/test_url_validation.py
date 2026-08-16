import pytest
from pydantic import ValidationError
from src.schemas.url import URLCreateRequest


def test_valid_urls():
    valid = URLCreateRequest(original_url="https://example.com/item/123")
    assert valid.original_url == "https://example.com/item/123"

    valid_custom = URLCreateRequest(
        original_url="http://sub.domain.org/page", custom_alias="my-alias_1"
    )
    assert valid_custom.custom_alias == "my-alias_1"


def test_invalid_scheme():
    with pytest.raises(ValidationError) as exc:
        URLCreateRequest(original_url="ftp://example.com/file.txt")
    assert "URL must start with http:// or https://" in str(exc.value)


def test_ssrf_prevention():
    invalid_hosts = [
        "http://localhost/admin",
        "http://127.0.0.1:8000/secret",
        "https://0.0.0.0/internal",
    ]
    for url in invalid_hosts:
        with pytest.raises(ValidationError):
            URLCreateRequest(original_url=url)


def test_invalid_custom_alias():
    with pytest.raises(ValidationError):
        URLCreateRequest(
            original_url="https://example.com", custom_alias="invalid alias!"
        )
