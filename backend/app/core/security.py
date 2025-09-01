"""Compatibility shim for security initialization.

Exports init_security from the enhanced security module so existing imports
from app.core.security continue to work.
"""

from app.core.security_enhanced import init_security  # re-export

__all__ = ["init_security"]


