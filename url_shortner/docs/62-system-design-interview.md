# 62 — System Design Interview Preparation Guide

## 1. Learning Objective
Prepare to ace Senior/Principal System Design Interviews for URL Shortener system design prompts.

---

## 2. Common System Design Interview Questions & Model Answers

### Question 1: "How do you handle 100,000 read requests per second on a viral link?"
**Model Answer**: 
> "I implement a multi-tiered caching strategy. At the edge, a CDN caches HTTP 302 redirects for non-expired links. At the application layer, worker processes maintain a local in-memory LRU cache for top viral keys, bypassing network trips. Finally, shared Redis clusters distribute read queries across shards using consistent hashing. Request coalescing (single-flight) prevents cache stampedes on cache misses."

### Question 2: "Why Base62 instead of Base64 or Hash Functions?"
**Model Answer**:
> "Base62 uses standard alphanumeric characters `[0-9a-zA-Z]`, which are completely URL-safe without requiring percent-encoding (`+` and `/` in Base64 can cause issues in query strings). Compared to MD5 hashing (which produces fixed 128-bit hashes requiring truncation and collision handling), Base62 encoding a 64-bit unique integer ID guarantees zero collisions and deterministic 7-character string outputs."
