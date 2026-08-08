import os
from dotenv import load_dotenv

load_dotenv()

class AppSettings:
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "super-secret-jwt-key-256bits-min-length-required-prod")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # Rate Limiting
    RATELIMIT_ENABLE: bool = os.getenv("RATELIMIT_ENABLE", "True").lower() in ("true", "1", "t")

settings = AppSettings()
