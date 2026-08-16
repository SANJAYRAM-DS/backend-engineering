import uuid
from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Index,
    String,
    Text,
)
from sqlalchemy.sql import func
from src.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class URL(Base):
    __tablename__ = "urls"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    short_code = Column(String(30), unique=True, index=True, nullable=False)
    original_url = Column(Text, nullable=False)
    user_id = Column(String(36), nullable=True, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expires_at = Column(DateTime(timezone=True), nullable=True)
    click_count = Column(BigInteger, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        Index("idx_urls_short_code_active", "short_code", "is_active"),
    )


class ClickEvent(Base):
    __tablename__ = "click_events"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    short_code = Column(String(30), nullable=False, index=True)
    clicked_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    referrer = Column(Text, nullable=True)
    country = Column(String(3), nullable=True)

    __table_args__ = (
        Index("idx_click_events_code_time", "short_code", "clicked_at"),
    )
