# 01 — Problem Understanding & Domain Fundamentals

# 01. Learning Objective

By the end of this document, I should understand:
- What a URL shortener system is and why businesses rely on short links.
- How HTTP Redirection status codes (`301` vs `302` vs `307` vs `308`) work under the hood.
- Why using `301 Moved Permanently` breaks link analytics and click tracking.
- The core user flows: URL Creation, URL Redirection, and Analytics inspection.
- The fundamental computer science and distributed system challenges in URL shortening.

---

# 02. Prerequisites

Before starting this document, I should understand:
- Basic HTTP client/server communication (Request/Response headers).
- Basic understanding of web browsers and URLs.

If you need refresher material, review:
- [docs/00-roadmap.md](file:///e:/backend_engineering/url_shortner/docs/00-roadmap.md)

---

# 03. Problem We Are Solving

Consider a modern marketing campaign sending embedded URLs via SMS or email:
`https://example.com/products/categories/electronics/item/1049285?referrer=email_campaign_2026&discount_code=SUMMER26`

Problems with this URL:
1. **SMS Character Capping**: SMS messages are capped at 160 characters. This single URL consumes 112 characters, forcing the campaign to span 2 SMS segments and doubling carrier billing costs.
2. **Visual Clutter**: Long URLs look untrustworthy, get truncated in social media posts, and generate dense, unscannable QR codes.
3. **Zero Telemetry Control**: Marketers cannot track who clicked the link, when they clicked, or revoke access if the promotion expires.

We need a system that maps this long URL to `https://short.ly/aB72x`.

---

# 04. Why This Problem Exists

Long URLs exist because modern RESTful web applications encode deep hierarchical paths, resource IDs, and query parameters directly into the URI string.

URL shorteners exist to act as an **indirection proxy layer**:

```text
[ Long Target URL ] ──(Mapped to)──> [ Short 7-Char Key ] ──(Stored in DB)──> [ Resolved via HTTP 302 ]
```

By placing an indirection proxy between the user and destination, we gain:
- Data compression (112 chars down to 20 chars).
- Telemetry interception (logging clicks, IP, user-agent).
- Dynamic destination editing (changing target URL without re-printing media).

---

# 05. Concept / Theory

### HTTP Redirection Mechanics (RFC 7231 / RFC 9110)

When a browser visits `https://short.ly/aB72x`:

```text
Client (Browser)                 URL Shortener API                 Target Destination
     │                                   │                                 │
     │─── GET /aB72x ───────────────────>│                                 │
     │                                   │ (Lookup Key "aB72x")            │
     │                                   │                                 │
     │<── 302 Found ─────────────────────│                                 │
     │    Location: https://example.com  │                                 │
     │                                   │                                 │
     │───────────────────────────────────┼────────────────────────────────>│
     │    GET https://example.com        │                                 │
```

---

# 06. How It Works Internally

### HTTP Status Codes Comparison

| Status Code | Header Name | Browser Caching Behavior | Analytics Impact | Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **`301 Moved Permanently`** | `Location` | **Aggressively cached by browser.** Subsequent visits bypass shortener server completely. | **Severely undercounts click analytics.** Only 1st click per browser is recorded! | Static domain migrations where server load reduction > analytics. |
| **`302 Found` (Temporary)** | `Location` | **Not cached by default.** Every click forces browser to send HTTP GET to shortener server. | **100% Accurate Click Analytics.** Server logs every click, IP, user-agent, and expiration. | **Standard URL Shorteners.** |
| **`307 Temporary Redirect`**| `Location` | Same as 302, guarantees HTTP Method cannot be altered (POST stays POST). | Accurate Analytics. | API proxy routing. |

---

# 07. Real-World Usage

- **Bitly / TinyURL / Dub.co**: Branded marketing short links & analytics dashboards.
- **Twitter/X (`t.co`)**: Shortening all shared links to save character limit and scan destinations for malware.
- **SMS Marketing & Print Media**: Keeping SMS segments short and QR codes low-density for camera scanning.

---

# 08. Requirements

- Redirection response MUST return `HTTP 302 Found` with `Location` header.
- Expired links MUST return `HTTP 404 Not Found`.

---

# 09. Architecture

```text
[ Client ] ──> GET /{short_code} ──> [ URL Shortener API ] ──> [ Database ]
                                              │
                                              v (Returns 302)
[ Client ] ─────────────────────────> [ Target Destination ]
```

---

# 10. Design Decisions

We choose **`302 Found`** over `301 Moved Permanently` because real-time click tracking, geolocation analytics, rate limiting, and dynamic link expiration are core requirements.

---

# 11. Alternatives

- **Client-Side JS Redirect (`<meta http-equiv="refresh">`)**: Slow (requires parsing HTML/JS engine), bad UX.
- **HTTP 301 Permanent Redirect**: Fast, but destroys analytics capability.
- **HTTP 302 Temporary Redirect**: Selected.

---

# 15. Step-by-Step Implementation

1. Read [02-requirements.md](file:///e:/backend_engineering/url_shortner/docs/02-requirements.md) for capacity estimation math.
2. Read [03-system-design.md](file:///e:/backend_engineering/url_shortner/docs/03-system-design.md) for architecture.

---

# 30. Interview Questions

1. **Why is `301` harmful for URL shortener analytics?**
   - *Answer*: Browsers cache 301 responses locally. Subsequent clicks go straight to destination without hitting the shortener server.
2. **What header specifies the target URL in an HTTP redirect?**
   - *Answer*: The `Location` HTTP response header.

---

# 33. Learning Checkpoint

- [ ] I understand what a URL shortener is.
- [ ] I can explain the difference between HTTP 301 and 302 redirects.
- [ ] I know why URL shorteners use 302 redirects.

---

# 34. Completion Checklist

- [ ] Read `01-problem-understanding.md`.
- [ ] Understood HTTP 302 mechanics.

---

# 35. What Comes Next

Next document: [docs/02-requirements.md](file:///e:/backend_engineering/url_shortner/docs/02-requirements.md)
