# Concept 21 — Security Engineering & Abuse Defense

# 1. Security Vectors & Defenses

- **Phishing & Malware**: Asynchronous target scanning via Google Safe Browsing API / VirusTotal.
- **SSRF Attacks**: Blocking target URLs attempting loopbacks to internal IPs (`127.0.0.1`, `169.254.169.254`).
- **SQL Injection**: Enforced ORM parameterized query binding.
- **Brute-Force Enumeration**: Rate limiting short code GET requests per IP.
