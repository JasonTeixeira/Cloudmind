#!/usr/bin/env python3
"""
Test Setup Script for CloudMind
Phase 1: Foundation Fixes
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_imports():
    """Test if all required modules can be imported"""
    try:
        # Test core imports
        import app.core.config
        import app.core.database
        import app.models
        import app.services
        import app.api
        
        logger.info("✅ All core modules imported successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Import error: {e}")
        return False


def test_database_connection():
    """Test database connection"""
    try:
        from app.core.database import engine
        from sqlalchemy import text
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


def test_models():
    """Test if models can be created"""
    try:
        from app.core.database import Base, engine
        
        # Test creating tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database models created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Model creation failed: {e}")
        return False


def test_config():
    """Test configuration loading"""
    try:
        from app.core.config import settings
        
        # Test basic settings
        assert settings.APP_NAME == "CloudMind"
        assert settings.ENVIRONMENT in ["development", "production"]
        
        logger.info("✅ Configuration loaded successfully")
        logger.info(f"   App Name: {settings.APP_NAME}")
        logger.info(f"   Environment: {settings.ENVIRONMENT}")
        logger.info(f"   Debug: {settings.DEBUG}")
        return True
    except Exception as e:
        logger.error(f"❌ Configuration test failed: {e}")
        return False


def test_directories():
    """Test if required directories exist"""
    try:
        directories = [
            "./storage",
            "./git-repos", 
            "./templates",
            "./backups",
            "./logs"
        ]
        
        for directory in directories:
            if not Path(directory).exists():
                logger.warning(f"⚠️ Directory missing: {directory}")
                Path(directory).mkdir(parents=True, exist_ok=True)
                logger.info(f"✅ Created directory: {directory}")
            else:
                logger.info(f"✅ Directory exists: {directory}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Directory test failed: {e}")
        return False


async def test_user_creation():
    """Test user creation"""
    try:
        from app.core.database import SessionLocal
        from app.services.user_service import UserService
        from app.schemas.user import UserCreate
        
        db = SessionLocal()
        user_service = UserService(db)
        
        # Test user data
        test_user_data = UserCreate(
            email="test@cloudmind.local",
            username="testuser",
            full_name="Test User",
            password="testpass123",
            role="viewer"
        )
        
        # Try to create user
        user = await user_service.create_user(test_user_data, created_by=None)
        
        if user:
            logger.info(f"✅ User creation successful: {user.email}")
            
            # Clean up test user
            db.delete(user)
            db.commit()
            logger.info("✅ Test user cleaned up")
        
        db.close()
        return True
    except Exception as e:
        logger.error(f"❌ User creation test failed: {e}")
        return False


def test_api_routes():
    """Test if API routes can be loaded"""
    try:
        from app.api.v1.api import api_router
        
        # Check if router has routes
        routes = list(api_router.routes)
        logger.info(f"✅ API routes loaded: {len(routes)} routes found")
        
        # List some key routes
        for route in routes[:5]:  # Show first 5 routes
            if hasattr(route, 'path'):
                logger.info(f"   - {route.path}")
        
        return True
    except Exception as e:
        logger.error(f"❌ API routes test failed: {e}")
        return False


async def main():
    """Main test function"""
    logger.info("🧪 CloudMind Setup Test")
    logger.info("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Test", test_config),
        ("Directory Test", test_directories),
        ("Database Connection Test", test_database_connection),
        ("Model Test", test_models),
        ("User Creation Test", test_user_creation),
        ("API Routes Test", test_api_routes),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n🔍 Running {test_name}...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} ERROR: {e}")
    
    logger.info("\n" + "=" * 50)
    logger.info(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! CloudMind is ready to run.")
        logger.info("📋 Next steps:")
        logger.info("   1. Run: python start_dev.py")
        logger.info("   2. Access: http://localhost:8000/docs")
        logger.info("   3. Login: admin@cloudmind.local / admin123")
    else:
        logger.error("❌ Some tests failed. Please fix the issues above.")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
