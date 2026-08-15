# 15 — Role-Based Access Control (RBAC)

## 1. Learning Objective
Design a Role-Based Access Control (RBAC) authorization matrix separating regular Users from System Administrators.

---

## 2. RBAC Matrix

| Role | Create Link | Delete Owned Link | Delete ANY Link | View Global System Metrics |
| :--- | :--- | :--- | :--- | :--- |
| **USER** | ✅ | ✅ | ❌ | ❌ |
| **ADMIN** | ✅ | ✅ | ✅ | ✅ |

---

## 3. Dependency Injection Guard in FastAPI

```python
def require_role(allowed_roles: list[str]):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Insufficient privileges")
        return current_user
    return role_checker
```
