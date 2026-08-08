# Phase 35: Technical Interview & Architecture Defense

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 35 of 35  
> **Target Path**: `docs/35-interview-prep.md`  

---

## 1. Executive Summary

Congratulations! You have completed the comprehensive architectural blueprint, code implementation, security hardening, and documentation for a **Production-Grade Authentication & Authorization System**.

This document equips you with the exact technical language, design trade-offs, and system design answers required to master Principal/Senior Backend Engineer technical interviews.

---

## 2. Master System Design Interview Scenarios

### Scenario A: "Design an Auth System for 100 Million Active Users"
* **Architectural Strategy**:
  1. **Stateless Access Token Verification**: Use short-lived (15m) asymmetric `RS256` signed JWTs so edge microservices verify tokens using public keys without hitting a central database.
  2. **Distributed Rate Limiting**: Deploy Redis Cluster with sliding window counter scripts to enforce rate limits across distributed API gateways.
  3. **Refresh Token Storage**: Store long-lived refresh tokens in PostgreSQL with database sharding based on `user_id` hash.
  4. **Instant Revocation**: Maintain an in-memory Redis Bloom Filter + Cache for revoked `jti` identifiers to ensure sub-millisecond blacklist lookups.

### Scenario B: "How Do You Handle Token Reuse and Hijacking?"
* **Architectural Strategy**:
  1. Implement **Refresh Token Rotation (RTR)**. Every refresh exchange invalidates the old token (`is_consumed = True`) and issues a new pair linked by a immutable `family_id`.
  2. If an attacker replays a previously consumed refresh token, the server immediately detects `is_consumed == True`.
  3. The system triggers **Family Revocation**: invalidating every refresh token sharing that `family_id`, logging out both legitimate user and attacker, and emitting a critical `SECURITY_BREACH_HIJACK_DETECTED` audit alert.

---

## 3. Top 10 Senior Engineering Interview Questions & Bulletproof Answers

#### Q1: Why use `HttpOnly` `SameSite=Lax` cookies for Refresh Tokens instead of LocalStorage?
* **Answer**: Storing tokens in `localStorage` exposes them to any JavaScript running on the page. If an XSS vulnerability occurs, malicious scripts can read `localStorage.getItem("token")` and exfiltrate credentials. `HttpOnly` cookies are inaccessible to JavaScript (`document.cookie` returns nothing), mitigating token theft from XSS. `SameSite=Lax` prevents CSRF attacks on top-level navigations.

#### Q2: What is the computational difference between `bcrypt` and standard hash functions like `SHA-256`?
* **Answer**: `SHA-256` is a fast cryptographic hash function designed for high throughput. Modern GPUs can calculate billions of SHA-256 hashes per second, making it vulnerable to brute-force cracking. `bcrypt` is an intentionally slow Key Derivation Function (KDF) with a configurable Work Factor (cost). It incorporates a 128-bit salt and requires significant memory and CPU cycles ($2^{12}$ iterations), reducing attacker cracking speeds to a few hundred hashes per second per GPU.

#### Q3: What is the difference between Symmetric (`HS256`) and Asymmetric (`RS256`) JWT Signing?
* **Answer**: `HS256` uses a single shared secret key for both signing and verifying tokens. Every microservice that needs to verify tokens must possess the secret key. If one service is compromised, tokens can be forged. `RS256` uses a private key for signing (kept secure on the Auth Service) and a public key for verification (distributed to all microservices). Microservices can verify authenticity without the ability to forge tokens.

#### Q4: How do you prevent User Enumeration attacks on Authentication Endpoints?
* **Answer**: 
  1. Return uniform error messages (e.g., `"Invalid email or password"`) for both incorrect emails and incorrect passwords.
  2. Enforce constant-time execution: if a submitted email does not exist, execute a dummy password hashing operation (`User().set_password(...)`) to match the ~100ms CPU execution delay of a real hash check, preventing timing attacks.
  3. On Password Reset requests, always return `HTTP 200 OK` with `"If the email exists, a reset link has been sent"`.

#### Q5: How do UUID primary keys improve security over auto-incrementing integer IDs?
* **Answer**: Integer primary keys (`1`, `2`, `3`) suffer from **Insecure Direct Object Reference (IDOR)** risks and sequential enumeration attacks. An attacker can iterate through `/api/v1/users/1`, `/api/v1/users/2` to scrape user data or measure business volume (e.g., total registered users). UUID v4 keys generate 128 bits of entropy, making primary key values unguessable ($2^{122}$ possible values).

---

## 4. Final Graduation Checklist

- [x] **Phase 01**: Requirements Analysis & System Design Blueprint
- [x] **Phase 02**: Authentication vs Authorization Paradigm
- [x] **Phase 03**: STRIDE Threat Modeling & Defense-in-Depth
- [x] **Phase 04**: PostgreSQL Normalized 3NF Relational Schema
- [x] **Phase 05**: Enterprise Clean Architecture Scaffolding
- [x] **Phase 06**: Environment & Secret Isolation
- [x] **Phase 07**: Custom User Model (`AbstractBaseUser` + UUID)
- [x] **Phase 08-09**: Registration Engine & Pydantic V2 Sanitation
- [x] **Phase 10**: Stateless Cryptographic Email Verification
- [x] **Phase 11-12**: Constant-Time Login & bcrypt Cryptography
- [x] **Phase 13-14**: JWT Architecture & Access Token Engine
- [x] **Phase 15-17**: Refresh Token Rotation (RTR) & Instant Blacklisting
- [x] **Phase 18-19**: Active Device Sessions & Dual Cookie Transport
- [x] **Phase 20**: Security Response Headers & Timing Middleware
- [x] **Phase 21-22**: Declarative Role-Based Access Control (RBAC)
- [x] **Phase 23**: Single-Use Cryptographic Password Reset
- [x] **Phase 24-25**: Structured JSON Logging & Immutable Audit Trail
- [x] **Phase 26-28**: Sliding Window Rate Limiting & Account Lockout
- [x] **Phase 29-30**: CORS Lockdown & Unified Exception Handlers
- [x] **Phase 31**: Pytest Test Suite with Fixtures & Mocking
- [x] **Phase 32-33**: Multi-Stage Docker Build & Production Hardening
- [x] **Phase 34**: OWASP API Top 10 Penetration Audit
- [x] **Phase 35**: Technical Interview & Architecture Defense Mastery

---
*End of Curriculum Documentation. You are now equipped with production-grade backend engineering knowledge.*
