# 04 — RESTful API Design & OpenAPI Specifications

# 01. Learning Objective

By the end of this document, I should understand:
- What RESTful API design principles are and how to design clean resource-oriented endpoints.
- Why HTTP verbs (`POST`, `GET`, `PUT`, `DELETE`) must be used correctly.
- How to structure standardized request bodies, response DTOs, and global error handling contracts.
- How to design endpoints for URL creation, HTTP 302 redirection, URL metadata, click analytics, and URL deletion.
- How to enforce API versioning (`/api/v1/`) and validation error handling.

---

# 02. Prerequisites

Before starting this document, I should understand:
- HTTP request/response methods, headers, and status codes from [01-problem-understanding.md](file:///e:/backend_engineering/url_shortner/docs/01-problem-understanding.md).
- System constraints from [02-requirements.md](file:///e:/backend_engineering/url_shortner/docs/02-requirements.md).
- Layered monolith architecture from [03-system-design.md](file:///e:/backend_engineering/url_shortner/docs/03-system-design.md).

---

# 03. Problem We Are Solving

When APIs are designed inconsistently (e.g., using `GET /create_url?target=...` or `POST /getLinkDetails`), front-end clients struggle with integration, browser caching breaks, security vulnerabilities emerge, and error handling becomes chaotic.

We need a standardized, versioned, RESTful OpenAPI contract for all client interactions.

---

# 04. Why This Problem Exists

In modern web & mobile architectures:
- **Inconsistent Routing**: Leads to broken API contracts and hard-to-debug client bugs.
- **Unstructured Error Messages**: Forces client applications to parse raw exception tracebacks or HTML pages instead of predictable JSON schemas.
- **Lack of Versioning**: Means updating an endpoint breaks backwards compatibility for existing mobile apps.

---

# 05. Concept / Theory

### RESTful API Naming Conventions & HTTP Verbs

1. **Plural Nouns**: Use `/api/v1/urls` instead of `/api/v1/createUrl`.
2. **HTTP Verbs**:
   - `POST /api/v1/urls`: Create a short URL resource.
   - `GET /{short_code}`: Resolve short code and return HTTP 302 redirect.
   - `GET /api/v1/urls/{short_code}`: Retrieve short link metadata.
   - `GET /api/v1/urls/{short_code}/analytics`: Retrieve link analytics.
   - `DELETE /api/v1/urls/{short_code}`: Soft-delete short URL resource.

---

# 06. How It Works Internally

### Standardized HTTP Status Code Contracts

| Status Code | Meaning | Occurs When |
| :--- | :--- | :--- |
| **`201 Created`** | Resource successfully generated | Short URL created successfully |
| **`302 Found`** | Temporary Redirection | Resolving short code to target URL |
| **`400 Bad Request`** | Input validation failure | Target URL malformed or > 2048 chars |
| **`404 Not Found`** | Resource missing or expired | Short code invalid or expired |
| **`409 Conflict`** | Resource conflict | Custom alias already in use |
| **`422 Unprocessable Entity`** | Structural schema validation error | Missing required request body parameters |
| **`429 Too Many Requests`** | Rate limit exceeded | Client exceeds request limit |

---

# 07. Real-World Usage

Enterprise APIs at companies like Stripe, GitHub, and Bitly strictly adhere to RESTful URI design, semantic HTTP status codes, and standardized JSON error structures.

---

# 08. Requirements

- All API endpoints must be prefixed with `/api/v1/`.
- All requests and responses must communicate via `Content-Type: application/json` (except redirection `302`).

---

# 09. Architecture

```text
[ Client ] ──> HTTP Request ──> [ FastAPI Router Layer ] ──> [ Service Layer ]
                                           │
                                           v (On Error)
                                [ Global Exception Handler ]
                                           │
                                           v
                                [ JSON Error Response ]
```

---

# 10. Design Decisions

- **API Prefix `/api/v1`**: Selected to allow future backwards-compatible `/api/v2` endpoints without breaking legacy API consumers.
- **Unified Error Response Schema**: Selected to ensure all errors return identical JSON objects across all endpoints.

---

# 11. Alternatives

- **GraphQL**: Flexible client querying, but introduces schema complexity and makes HTTP-level redirection caching difficult.
- **gRPC**: Binary Protocol Buffer RPCs, ultra-fast internal microservice communication, but unsuitable for direct browser short link redirection.

---

# 13. API Changes & Endpoint Contracts

### Endpoint 1: Create Short URL
- **Method / Path**: `POST /api/v1/urls`
- **Request Body**:
  ```json
  {
    "original_url": "https://example.com/very/long/path",
    "custom_alias": "my-deal",
    "expires_at": "2026-12-31T23:59:59Z"
  }
  ```
- **Response (`201 Created`)**:
  ```json
  {
    "short_code": "my-deal",
    "short_url": "http://localhost:8000/my-deal",
    "original_url": "https://example.com/very/long/path",
    "created_at": "2026-08-15T09:00:00Z",
    "expires_at": "2026-12-31T23:59:59Z",
    "click_count": 0,
    "is_active": true
  }
  ```

### Endpoint 2: Resolve Short URL
- **Method / Path**: `GET /{short_code}`
- **Response (`302 Found`)**:
  ```http
  HTTP/1.1 302 Found
  Location: https://example.com/very/long/path
  ```

---

# 14. Folder/File Changes

Files implementing API Contracts:
- `src/schemas/url.py` — Pydantic Request/Response DTOs
- `src/api/v1/urls.py` — FastAPI Router handlers

---

# 15. Step-by-Step Implementation

1. Implement `URLCreateRequest`, `URLResponse`, and `AnalyticsResponse` inside `src/schemas/url.py`.
2. Implement route handlers in `src/api/v1/urls.py`.
3. Register router inside `src/main.py`.

---

# 16. Complete Code

### Pydantic Schemas (`src/schemas/url.py`)
```python
import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class URLCreateRequest(BaseModel):
    original_url: str = Field(
        ...,
        description="Target destination URL to shorten",
        example="https://example.com/products/item123",
    )
    custom_alias: Optional[str] = Field(
        None,
        min_length=3,
        max_length=30,
        description="Optional custom text alias for short URL",
        example="my-deal",
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
```

---

# 21. Expected Output

### Manual Verification via Curl
```bash
curl -X POST "http://localhost:8000/api/v1/urls" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://example.com"}'
```
Expected Status: `201 Created`

---

# 30. Interview Questions

1. **Why should API endpoints use plural nouns (`/urls`) instead of verbs (`/create_url`)?**
   - *Answer*: REST treats resources as entities. HTTP verbs (`POST`, `GET`, `DELETE`) represent actions performed on those resources.
2. **What HTTP status code should be returned when a custom alias is already taken?**
   - *Answer*: `409 Conflict`.

---

# 33. Learning Checkpoint

- [ ] I can design RESTful API contracts.
- [ ] I know how to use Pydantic for input validation.
- [ ] I understand standard HTTP status codes.

---

# 35. What Comes Next

Next document: [docs/05-database-design.md](file:///e:/backend_engineering/url_shortner/docs/05-database-design.md)
