import datetime
import ipaddress
from typing import Optional
from urllib.parse import urlparse
from pydantic import BaseModel, Field, field_validator


FORBIDDEN_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}


class URLCreateRequest(BaseModel):
    original_url: str = Field(
        ...,
        description="Target destination URL to shorten",
        json_schema_extra={"example": "https://example.com/products/item123"},
    )
    custom_alias: Optional[str] = Field(
        None,
        min_length=3,
        max_length=30,
        description="Optional custom text alias for short URL",
        json_schema_extra={"example": "my-deal"},
    )
    expires_at: Optional[datetime.datetime] = Field(
        None, description="Optional ISO-8601 expiration date"
    )

    @field_validator("original_url")
    @classmethod
    def validate_original_url(cls, v: str) -> str:
        v_stripped = v.strip()
        if not (v_stripped.startswith("http://") or v_stripped.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        if len(v_stripped) > 2048:
            raise ValueError("URL length exceeds 2048 characters limit")

        parsed = urlparse(v_stripped)
        hostname = (parsed.hostname or "").lower()

        if hostname in FORBIDDEN_HOSTS:
            raise ValueError("Cannot shorten loopback or localhost addresses")

        # Try to parse as IP address and check if private
        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_link_local:
                raise ValueError("Cannot shorten private or loopback IP addresses")
        except ValueError:
            # Not an IP address string, hostname is domain name
            pass

        return v_stripped

    @field_validator("custom_alias")
    @classmethod
    def validate_custom_alias(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v_stripped = v.strip()
        if not all(c.isalnum() or c in "-_" for c in v_stripped):
            raise ValueError(
                "Custom alias must contain only alphanumeric characters, hyphens, or underscores"
            )
        return v_stripped


class URLResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    created_at: datetime.datetime
    expires_at: Optional[datetime.datetime] = None
    click_count: int = 0
    is_active: bool = True

    class Config:
        from_attributes = True


class AnalyticsResponse(BaseModel):
    short_code: str
    original_url: str
    total_clicks: int
    created_at: datetime.datetime
    expires_at: Optional[datetime.datetime] = None
    is_active: bool