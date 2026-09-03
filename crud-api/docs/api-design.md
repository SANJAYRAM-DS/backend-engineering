# ResourceHub — REST API Specification

## 1. General API Principles
* **Protocol:** HTTPS
* **Base URL:** `/api/v1`
* **Format:** JSON (`Content-Type: application/json`)
* **Authentication:** Bearer JWT in Request Header (`Authorization: Bearer <access_token>`)
* **Statelessness:** No server-side HTTP session state; every request contains all credentials necessary.

---

## 2. Standard Response & Error Envelope

### Success Response Envelope
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### Error Response Envelope
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Task with ID 'tks_987' was not found.",
    "details": [
      {
        "field": "task_id",
        "issue": "No matching record in database."
      }
    ]
  }
}
```

---

## 3. Standard HTTP Status Codes

| Code | Status | Usage |
| :--- | :--- | :--- |
| `200 OK` | Success | Standard successful response for GET, PATCH, PUT. |
| `201 Created` | Created | Resource successfully created (POST). |
| `204 No Content` | Deleted | Resource deleted successfully (DELETE). No body returned. |
| `400 Bad Request` | Client Error | Malformed request syntax or invalid input payload. |
| `401 Unauthorized` | Auth Error | Missing, invalid, or expired JWT access token. |
| `403 Forbidden` | Permission Error | User authenticated, but lacks RBAC role permissions. |
| `404 Not Found` | Not Found | Requested URI path or database resource does not exist. |
| `409 Conflict` | Business Conflict | Unique constraint violation (e.g., email already registered). |
| `422 Unprocessable` | Validation Error | Pydantic type/field validation failure. |
| `500 Internal Error` | Server Error | Unexpected internal server fault. |

---

## 4. REST Endpoint Specifications

### 4.1 Authentication & Profile (`/auth`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register a new user account | Public |
| `POST` | `/api/v1/auth/login` | Authenticate user & return JWT tokens | Public |
| `POST` | `/api/v1/auth/refresh` | Issue new access token using refresh token | Public |
| `GET` | `/api/v1/auth/me` | Fetch currently authenticated user profile | Bearer Token |

### 4.2 Projects (`/projects`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/projects` | Create a new project (Caller becomes OWNER) | Bearer Token |
| `GET` | `/api/v1/projects` | List projects where caller is Owner/Member | Bearer Token |
| `GET` | `/api/v1/projects/{project_id}` | Get detailed project metadata | Bearer Token |
| `PATCH` | `/api/v1/projects/{project_id}` | Update project metadata (OWNER, ADMIN) | Bearer Token |
| `DELETE` | `/api/v1/projects/{project_id}` | Delete project & cascading entities (OWNER) | Bearer Token |

### 4.3 Project Members & RBAC (`/projects/{project_id}/members`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/projects/{project_id}/members` | Add user to project with role | Bearer Token (OWNER/ADMIN) |
| `GET` | `/api/v1/projects/{project_id}/members` | List members of a project | Bearer Token |
| `PATCH` | `/api/v1/projects/{project_id}/members/{user_id}` | Update member role | Bearer Token (OWNER) |
| `DELETE` | `/api/v1/projects/{project_id}/members/{user_id}` | Remove member from project | Bearer Token (OWNER/ADMIN) |

### 4.4 Tasks (`/projects/{project_id}/tasks` & `/tasks/{task_id}`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/projects/{project_id}/tasks` | Create a new task under project | Bearer Token |
| `GET` | `/api/v1/projects/{project_id}/tasks` | List, search, filter, and sort tasks | Bearer Token |
| `GET` | `/api/v1/tasks/{task_id}` | Get task details by ID | Bearer Token |
| `PATCH` | `/api/v1/tasks/{task_id}` | Update task (fields, assignee, status) | Bearer Token |
| `DELETE` | `/api/v1/tasks/{task_id}` | Delete task | Bearer Token |

#### Query Parameters for Task Filtering, Searching, & Sorting (`GET /api/v1/projects/{project_id}/tasks`)
* `q` *(string)*: Search term for task title and description full-text search.
* `status` *(string)*: Filter by task status (`TODO`, `IN_PROGRESS`, `IN_REVIEW`, `COMPLETED`, `ARCHIVED`).
* `priority` *(string)*: Filter by priority (`LOW`, `MEDIUM`, `HIGH`, `URGENT`).
* `assignee_id` *(uuid)*: Filter by assigned user UUID.
* `sort_by` *(string)*: Field to sort by (`created_at`, `due_date`, `priority`, `title`). Default: `created_at`.
* `order` *(string)*: Sort direction (`asc`, `desc`). Default: `desc`.
* `page` *(integer)*: Page number (1-indexed). Default: `1`.
* `limit` *(integer)*: Page size limit. Default: `20`, Max: `100`.

### 4.5 Task Comments (`/tasks/{task_id}/comments`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/tasks/{task_id}/comments` | Post a comment on a task | Bearer Token |
| `GET` | `/api/v1/tasks/{task_id}/comments` | Retrieve paginated comments for task | Bearer Token |
| `PATCH` | `/api/v1/comments/{comment_id}` | Update own comment content | Bearer Token |
| `DELETE` | `/api/v1/comments/{comment_id}` | Delete comment | Bearer Token |

### 4.6 Activity Logs (`/projects/{project_id}/activity`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/projects/{project_id}/activity` | Fetch paginated audit event stream | Bearer Token |
