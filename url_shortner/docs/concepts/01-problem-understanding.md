# Concept 01 — Problem Understanding & Indirection Proxy Mechanics

# 1. Problem
Consider a long URL:
`https://example.com/products/category/electronics/product/12345?referrer=email_campaign_2026&discount=SUMMER26`

When shared across SMS, print media, social media posts, or QR codes:
- It consumes 105 characters (over 65% of a 160-character SMS segment).
- It produces a dense, un-scannable QR code.
- It provides zero click tracking or analytics control.

We want to transform it into: `https://short.ly/aB72x`

When someone performs `GET /aB72x`, the system resolves `aB72x -> original URL` and redirects the user client.

---

# 2. Engineering Questions to Ask
- What HTTP status code should be used for redirection (`301` vs `302`)?
- How is `aB72x` generated to guarantee zero collisions?
- What happens when 100,000 users click `short.ly/aB72x` simultaneously?
- How do we log click count, country, and device type without slowing down the redirect?

---

# 3. Core Mechanics

```text
[ Client (Browser) ] ─── GET /aB72x ───> [ URL Shortener API ]
                                                  │
                                                  │ (DB / Cache Lookup)
                                                  v
[ Client (Browser) ] <── 302 Found ───────────────┘
                         Location: https://example.com/products/...
```

### HTTP Status Code Impact
- **`301 Moved Permanently`**: Browser caches the redirection locally. Subsequent clicks bypass our server entirely. **Analytics are broken after the 1st click.**
- **`302 Found`**: Browser does not cache redirect. Every click hits our server. **Guarantees 100% accurate click analytics and real-time link revocation.**

---

# 4. Real-World Applications
- **SMS Marketing**: Capping link lengths to save cellular SMS billing costs.
- **Bitly / Dub.co**: Branded marketing links, conversion telemetry.
- **Twitter/X (`t.co`)**: Shortening all links to preserve tweet character limits and scan destinations for malware.
