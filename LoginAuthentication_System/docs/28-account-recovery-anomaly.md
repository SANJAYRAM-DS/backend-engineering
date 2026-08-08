# Phase 28: Account Recovery & Anomaly Detection

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 28 of 35  
> **Target Path**: `docs/28-account-recovery-anomaly.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Building an Anomaly Detection Engine that monitors login requests for unusual security patterns.
* Tracking device fingerprints, novel User-Agent strings, geographic IP shifts, and impossible travel velocity.
* Triggering adaptive Step-Up Authentication (MFA / Email OTP verification) when high anomaly risk scores are detected.
* Designing emergency account recovery workflows for users whose credentials or devices have been compromised.

---

## 2. Risk-Based Adaptive Authentication Flow

```mermaid
flowchart TD
    Req["Incoming Login Request"] --> Extract["Extract IP, GeoLocation, Device Fingerprint"]
    Extract --> Compute["Compute Risk Score (0 - 100)"]
    Compute --> ScoreCheck{"Risk Score Threshold?"}
    ScoreCheck -->|Score < 30 (Low Risk)| Allow["Standard Login Proceed"]
    ScoreCheck -->|30 <= Score < 70 (Medium)| StepUp["Trigger Step-Up Auth (Email OTP / MFA)"]
    ScoreCheck -->|Score >= 70 (High Risk)| Block["Block Request & Notify User Email"]
```

---

## 3. Production Anomaly Detection Engine

File path: `core/security/anomaly.py`

```python
"""
Risk-Based Anomaly Detection and Device Fingerprinting Engine.
"""
from typing import Tuple, Dict, Any
from django.core.cache import cache
import logging

logger = logging.getLogger("security.anomaly")


class AnomalyDetectionEngine:

    RISK_THRESHOLD_STEPUP = 30
    RISK_THRESHOLD_BLOCK = 75

    @classmethod
    def evaluate_request_risk(
        cls, 
        user_id: str, 
        current_ip: str, 
        current_user_agent: str,
        geo_country: str = "UNKNOWN"
    ) -> Tuple[int, Dict[str, Any]]:
        """
        Evaluates login anomaly risk based on historic device and IP history.
        Returns a Risk Score tuple: (score, risk_factors)
        """
        risk_score = 0
        risk_factors = {}

        history_key = f"user_device_history:{user_id}"
        history = cache.get(history_key, {"ips": set(), "user_agents": set(), "countries": set()})

        # 1. Check for Unknown IP Address
        if current_ip not in history.get("ips", set()):
            risk_score += 20
            risk_factors["new_ip"] = True

        # 2. Check for Unknown User-Agent / Device
        if current_user_agent not in history.get("user_agents", set()):
            risk_score += 25
            risk_factors["new_device_user_agent"] = True

        # 3. Check for Impossible Travel / Foreign Country Shift
        if geo_country != "UNKNOWN" and geo_country not in history.get("countries", set()):
            risk_score += 35
            risk_factors["new_geographic_country"] = True

        logger.info(f"ANOMALY_EVAL: User {user_id} Score={risk_score} Factors={risk_factors}")
        return risk_score, risk_factors

    @classmethod
    def record_trusted_context(
        cls, 
        user_id: str, 
        ip: str, 
        user_agent: str, 
        country: str = "UNKNOWN"
    ) -> None:
        """
        Saves a successfully verified device/IP into the user's historical trust profile.
        """
        history_key = f"user_device_history:{user_id}"
        history = cache.get(history_key, {"ips": set(), "user_agents": set(), "countries": set()})
        
        history["ips"].add(ip)
        history["user_agents"].add(user_agent)
        if country != "UNKNOWN":
            history["countries"].add(country)

        # Retain history in cache for 90 days
        cache.set(history_key, history, timeout=7776000)
```

---

## 4. Mentor Mode: Self-Check & Exercises

### Self-Check Questions
1. **What is "Impossible Travel Velocity" in backend security monitoring?**  
   *Answer: Impossible travel occurs when a user logs in from New York at 10:00 AM and from Tokyo at 10:30 AM. Because physical travel between those locations is impossible within 30 minutes, it indicates compromised credentials.*

2. **How does adaptive step-up authentication improve both user experience and security?**  
   *Answer: Standard users logging in from trusted daily devices experience frictionless single-factor authentication, while high-risk requests trigger mandatory secondary verification steps (MFA/OTP).*

### Practical Exercise
* Implement an API endpoint `/api/v1/auth/recovery/emergency-lock` that allows a user to click a link in a "New Device Login" email alert to instantly terminate all sessions and lock their account.
