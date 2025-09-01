"""
Cryptography utilities
"""
import hashlib
import secrets
from typing import Optional

def generate_secure_token(length: int = 32) -> str:
    """Generate a secure random token"""
    return secrets.token_urlsafe(length)

def hash_password(password: str) -> str:
    """Hash a password securely"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    return hash_password(password) == hashed
