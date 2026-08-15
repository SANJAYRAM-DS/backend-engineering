# Concept 04 — RESTful API Design & OpenAPI Semantics

# 1. Core API Contracts

```http
POST /api/v1/urls
GET /{short_code}
GET /api/v1/urls/{short_code}
GET /api/v1/urls/{short_code}/analytics
DELETE /api/v1/urls/{short_code}
```

---

# 2. Request & Response Payload Examples

### 2.1 Create Short URL
- **`POST /api/v1/urls`**
- **Request Body**:
  ```json
  {
    "original_url": "https://example.com/very/long/url",
    "custom_alias": "summer-sale",
    "expires_at": "2026-12-31T23:59:59Z"
  }
  ```
- **Response (`201 Created`)**:
  ```json
  {
    "short_code": "summer-sale",
    "short_url": "http://localhost:8000/summer-sale",
    "original_url": "https://example.com/very/long/url",
    "created_at": "2026-08-15T09:00:00Z"
  }
  ```

### 2.2 Redirection Response
- **`GET /summer-sale`**
- **Response (`302 Found`)**:
  ```http
  HTTP/1.1 302 Found
  Location: https://example.com/very/long/url
  ```

---

# 3. Key Concepts Taught
- **REST Resource Orientated Nouns**: Using plural nouns (`/urls`) rather than action verbs (`/createUrl`).
- **HTTP Status Semantics**: `201` (Created), `302` (Found), `400` (Bad Request), `404` (Not Found), `409` (Conflict), `429` (Rate Limited).
- **API Versioning**: Prefixing `/api/v1/` to protect backwards compatibility.
