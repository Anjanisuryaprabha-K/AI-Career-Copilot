from fastapi import Header, HTTPException, status
from typing import Optional, Dict, Any
from app.utils.security import decode_access_token
from app.repositories.user_repository import user_repository


async def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Missing or invalid Bearer token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = authorization.split(" ")[1].strip()
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has expired or token is invalid. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = payload.get("sub")
    email = payload.get("email")

    user = None
    if user_id:
        user = await user_repository.get_by_id(str(user_id))
    if not user and email:
        user = await user_repository.get_by_email(email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User associated with this session token no longer exists. Please sign in again."
        )

    user["id"] = str(user.get("_id", user_id or ""))
    return user


async def get_optional_user(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    try:
        return await get_current_user(authorization)
    except HTTPException:
        return None


def resolve_user_id(user: Optional[Dict[str, Any]], default: str = "demo_usr") -> str:
    """
    Extract a consistent user_id string from an authenticated (or None) user dict.

    Centralizes the repeated one-liner used across all routers:
        str(user.get("_id", user.get("id", "demo_usr"))) if user else "demo_usr"
    """
    if not user:
        return default
    return str(user.get("_id", user.get("id", default)))
