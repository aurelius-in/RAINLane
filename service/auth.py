import os
from typing import Optional
from fastapi import Header, HTTPException


def _load_keys() -> list[str]:
    raw = os.getenv("RAINLANE_API_KEYS", "").strip()
    if not raw:
        return []
    return [k.strip() for k in raw.split(",") if k.strip()]


def require_api_key(x_api_key: Optional[str] = Header(default=None)) -> str:
    allowed = _load_keys()
    # If no keys configured, allow all (dev mode)
    if not allowed:
        return x_api_key or "anonymous"
    if not x_api_key or x_api_key not in allowed:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_api_key


