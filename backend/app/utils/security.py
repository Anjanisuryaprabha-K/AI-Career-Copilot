import re
import hashlib
import secrets
import json
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from app.config import settings

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def is_valid_email_format(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        if not hashed_password or '$' not in hashed_password:
            return False
        salt, stored_hash = hashed_password.split('$', 1)
        computed_key = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return computed_key.hex() == stored_hash
    except Exception:
        return False

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    header = {"alg": settings.JWT_ALGORITHM, "typ": "JWT"}
    payload = dict(data)
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload["iat"] = now.timestamp()
    payload["exp"] = expire.timestamp()
    
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    
    signature_raw = f"{header_b64}.{payload_b64}.{settings.JWT_SECRET}".encode('utf-8')
    signature = hashlib.sha256(signature_raw).hexdigest()
    return f"{header_b64}.{payload_b64}.{signature}"

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        header_b64, payload_b64, signature = parts
        signature_raw = f"{header_b64}.{payload_b64}.{settings.JWT_SECRET}".encode('utf-8')
        expected_sig = hashlib.sha256(signature_raw).hexdigest()
        if signature != expected_sig:
            return None
        
        # Add padding back if necessary
        padded_payload = payload_b64 + '=' * ((4 - len(payload_b64) % 4) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded_payload.encode()).decode())
        
        if datetime.utcnow().timestamp() > payload.get("exp", 0):
            return None # Expired
        return payload
    except Exception:
        return None
