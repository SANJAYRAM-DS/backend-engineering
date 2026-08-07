# Phase 34: Penetration Testing & OWASP Review

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 34 of 35  
> **Target Path**: `docs/34-pen-testing-owasp.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Conducting automated and manual security audits against the **OWASP API Security Top 10 (2023)**.
* Testing authentication endpoints for JWT algorithm confusion, signature bypass, and timing attacks.
* Verifying zero data leakage in production exception responses.

---

## 2. OWASP API Top 10 Penetration Audit Checklist

| Vulnerability Code | Description | Automated Penetration Test Verification Step | Audit Result |
| :--- | :--- | :--- | :--- |
| **API1:2023** | Broken Object Level Authorization (BOLA) | Swap target UUID in `GET /users/{uuid}` with non-owned user ID. | **PASS**: Returns 403 Forbidden |
| **API2:2023** | Broken Authentication | Submit expired/tampered JWT tokens & `"alg": "none"` payload. | **PASS**: Returns 401 Unauthorized |
| **API3:2023** | Broken Object Property Level Authorization | Submit `"is_superuser": true` during registration POST. | **PASS**: Pydantic schema strips invalid keys |
| **API4:2023** | Unrestricted Resource Consumption | Flood login endpoint with 100 rapid requests. | **PASS**: Rate limiter triggers 429 Too Many Requests |
| **API5:2023** | Broken Function Level Authorization | Standard user calls `DELETE /api/v1/roles/{id}`. | **PASS**: Returns 403 Forbidden |
| **API7:2023** | Server Side Request Forgery (SSRF) | Pass external URLs in callback fields. | **PASS**: URLs strictly validated against allowlist |
| **API8:2023** | Security Misconfiguration | Inspect HTTP headers for missing HSTS/CSP or debug stack traces. | **PASS**: Debug=False, Security headers present |
| **API9:2023** | Improper Inventory Management | Query old API versions `/api/v0/login`. | **PASS**: Deprecated endpoints removed |

---

## 3. Mentor Mode: Self-Check

### Self-Check Questions
1. How does testing for `"alg": "none"` in JWT header parsing protect against legacy JWT library bugs?  
   *Answer: Early JWT libraries improperly accepted `"alg": "none"`, verifying signatures as valid even if signature bytes were removed. Modern `PyJWT` explicitly rejects `"alg": "none"` unless explicitly enabled.*
