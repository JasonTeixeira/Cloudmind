"""
Multi-Factor Authentication (MFA) Models
Enterprise-grade MFA implementation for CloudMind
"""

import logging
import secrets
import qrcode
import io
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from enum import Enum

from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID

from app.core.database import Base

logger = logging.getLogger(__name__)


class MFAMethod(str, Enum):
    """MFA method enumeration"""
    TOTP = "totp"  # Time-based One-Time Password
    SMS = "sms"    # SMS verification
    EMAIL = "email"  # Email verification
    BACKUP = "backup"  # Backup codes
    HARDWARE = "hardware"  # Hardware tokens


class MFAStatus(str, Enum):
    """MFA status enumeration"""
    PENDING = "pending"
    ACTIVE = "active"
    DISABLED = "disabled"
    LOCKED = "locked"


class MFASecret(Base):
    """MFA secrets and configuration"""
    
    __tablename__ = "mfa_secrets"
    
    id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # TOTP Configuration
    totp_secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    totp_algorithm: Mapped[str] = mapped_column(String(20), default="SHA1", nullable=False)
    totp_digits: Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    totp_period: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    
    # Backup Codes
    backup_codes: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    
    # SMS/Email Configuration
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Hardware Token
    hardware_token_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Status and Settings
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    mfa_method: Mapped[MFAMethod] = mapped_column(String(20), default=MFAMethod.TOTP, nullable=False)
    mfa_status: Mapped[MFAStatus] = mapped_column(String(20), default=MFAStatus.PENDING, nullable=False)
    
    # Security Settings
    require_mfa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    grace_period_days: Mapped[int] = mapped_column(Integer, default=7, nullable=False)
    max_failed_attempts: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    lockout_duration_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="mfa_secrets")
    mfa_attempts = relationship("MFAAttempt", back_populates="mfa_secret", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<MFASecret(id={self.id}, user_id={self.user_id}, method='{self.mfa_method}')>"
    
    def generate_totp_secret(self) -> str:
        """Generate a new TOTP secret"""
        self.totp_secret = base64.b32encode(secrets.token_bytes(20)).decode('utf-8')
        return self.totp_secret
    
    def generate_backup_codes(self, count: int = 10) -> list:
        """Generate backup codes"""
        codes = []
        for _ in range(count):
            code = secrets.token_hex(4).upper()  # 8-character hex code
            codes.append(code)
        
        self.backup_codes = {
            "codes": codes,
            "used_codes": [],
            "generated_at": datetime.utcnow().isoformat()
        }
        return codes
    
    def verify_backup_code(self, code: str) -> bool:
        """Verify a backup code"""
        if not self.backup_codes or "codes" not in self.backup_codes:
            return False
        
        code = code.upper()
        if code in self.backup_codes["codes"]:
            # Mark code as used
            self.backup_codes["codes"].remove(code)
            self.backup_codes["used_codes"].append(code)
            self.last_used_at = datetime.utcnow()
            return True
        
        return False
    
    def get_qr_code_data(self) -> str:
        """Generate QR code data for TOTP setup"""
        if not self.totp_secret:
            return ""
        
        # Generate TOTP URI
        totp_uri = f"otpauth://totp/CloudMind:{self.user.email}?secret={self.totp_secret}&issuer=CloudMind&algorithm={self.totp_algorithm}&digits={self.totp_digits}&period={self.totp_period}"
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    def is_locked(self) -> bool:
        """Check if MFA is locked due to failed attempts"""
        if not self.mfa_attempts:
            return False
        
        recent_failures = [
            attempt for attempt in self.mfa_attempts
            if attempt.failed and attempt.created_at > datetime.utcnow() - timedelta(minutes=self.lockout_duration_minutes)
        ]
        
        return len(recent_failures) >= self.max_failed_attempts
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "mfa_enabled": self.mfa_enabled,
            "mfa_method": self.mfa_method,
            "mfa_status": self.mfa_status,
            "require_mfa": self.require_mfa,
            "grace_period_days": self.grace_period_days,
            "max_failed_attempts": self.max_failed_attempts,
            "lockout_duration_minutes": self.lockout_duration_minutes,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_locked": self.is_locked(),
            "backup_codes_remaining": len(self.backup_codes.get("codes", [])) if self.backup_codes else 0
        }


class MFAAttempt(Base):
    """MFA verification attempts"""
    
    __tablename__ = "mfa_attempts"
    
    id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    mfa_secret_id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), ForeignKey("mfa_secrets.id"), nullable=False)
    
    # Attempt details
    method: Mapped[MFAMethod] = mapped_column(String(20), nullable=False)
    code: Mapped[str] = mapped_column(String(255), nullable=False)
    failed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Security information
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    mfa_secret = relationship("MFASecret", back_populates="mfa_attempts")
    
    def __repr__(self):
        return f"<MFAAttempt(id={self.id}, method='{self.method}', failed={self.failed})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "mfa_secret_id": str(self.mfa_secret_id),
            "method": self.method,
            "failed": self.failed,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "location": self.location,
            "created_at": self.created_at.isoformat()
        }


class MFASession(Base):
    """MFA session management"""
    
    __tablename__ = "mfa_sessions"
    
    id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Session details
    session_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    device_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    device_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Trust settings
    trusted_device: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    remember_device: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Security information
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="mfa_sessions")
    
    def __repr__(self):
        return f"<MFASession(id={self.id}, user_id={self.user_id}, trusted={self.trusted_device})>"
    
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "device_id": self.device_id,
            "device_name": self.device_name,
            "trusted_device": self.trusted_device,
            "remember_device": self.remember_device,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "location": self.location,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat(),
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "is_expired": self.is_expired()
        } 