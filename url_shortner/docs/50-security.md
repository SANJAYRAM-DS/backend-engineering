# 50 & 51 — Security Hardening & Malware/Phishing Abuse Prevention

## 1. Learning Objective
Analyze security attack vectors against URL shorteners (Phishing, Spam, Botnet scanning, SSRF, SQL Injection, XSS) and implement threat defenses.

---

## 2. Security Threat Defense Matrix

| Threat Vector | Attack Mechanism | Countermeasure |
| :--- | :--- | :--- |
| **Phishing / Malware** | User shortens link to malware domain (`malware.example/payload.exe`) | Asynchronous integration with Google Safe Browsing API / VirusTotal scanner. |
| **Brute-Force Enumeration** | Crawler iterates `GET /aB700`, `/aB701` to find active links | Rate limiting, CAPTCHA on creation, 64-bit non-sequential short code generation. |
| **SSRF Attack** | Shortens `http://169.254.169.254/latest/meta-data/` to read AWS cloud secrets | Strict IP CIDR block validation preventing private IP destinations. |
