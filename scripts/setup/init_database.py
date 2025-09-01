#!/usr/bin/env python3
"""
Database Initialization Script for CloudMind
Phase 1: Foundation Fixes
"""

import os
import sys
import logging
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.core.database import Base, engine, SessionLocal
from app.core.config import settings
from app.models import *  # Import all models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_database_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            logger.info("✅ Database connection successful")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


def create_database_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {e}")
        return False


def create_sqlite_fallback():
    """Create SQLite database as fallback"""
    try:
        sqlite_engine = create_engine("sqlite:///./cloudmind.db")
        Base.metadata.create_all(bind=sqlite_engine)
        logger.info("✅ SQLite database created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create SQLite database: {e}")
        return False


def create_initial_data():
    """Create initial data for development"""
    try:
        db = SessionLocal()
        
        # Check if we already have users
        from app.models.user import User
        existing_users = db.query(User).count()
        
        if existing_users == 0:
            logger.info("📝 Creating initial development data...")
            
            # Create a master user
            from app.services.user_service import UserService
            from app.schemas.user import UserCreate
            user_service = UserService(db)
            
            master_user_data = UserCreate(
                email="admin@cloudmind.local",
                username="admin",
                full_name="CloudMind Administrator",
                password="admin123",  # Change this in production!
                role="master",
                is_master_user=True,
                is_superuser=True,
                is_verified=True
            )
            
            master_user = await user_service.create_user(master_user_data, created_by=None)
            
            logger.info(f"✅ Created master user: {master_user.email}")
            
            # Create a sample project
            from app.models.project import Project
            sample_project = Project(
                name="Sample Cloud Project",
                description="A sample project for testing CloudMind features",
                slug="sample-project",
                owner_id=master_user.id,
                is_public=True,
                cloud_providers=["aws", "azure", "gcp"],
                regions=["us-east-1", "us-west-2", "eu-west-1"],
                monthly_budget=10000  # $100/month
            )
            
            db.add(sample_project)
            db.commit()
            
            logger.info(f"✅ Created sample project: {sample_project.name}")
        
        db.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create initial data: {e}")
        return False


def setup_directories():
    """Create necessary directories"""
    try:
        directories = [
            "./storage",
            "./git-repos", 
            "./templates",
            "./backups",
            "./logs"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"✅ Created directory: {directory}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create directories: {e}")
        return False


def main():
    """Main initialization function"""
    logger.info("🚀 Starting CloudMind database initialization...")
    
    # Step 1: Test database connection
    if not test_database_connection():
        logger.warning("⚠️ Primary database connection failed, using SQLite fallback")
        if not create_sqlite_fallback():
            logger.error("❌ Failed to create any database")
            return False
    
    # Step 2: Create database tables
    if not create_database_tables():
        logger.error("❌ Failed to create database tables")
        return False
    
    # Step 3: Create directories
    if not setup_directories():
        logger.error("❌ Failed to create directories")
        return False
    
    # Step 4: Create initial data
    if not create_initial_data():
        logger.error("❌ Failed to create initial data")
        return False
    
    logger.info("🎉 Database initialization completed successfully!")
    logger.info("📋 Next steps:")
    logger.info("   1. Start the backend server: python -m uvicorn app.main:app --reload")
    logger.info("   2. Access the API docs: http://localhost:8000/docs")
    logger.info("   3. Login with: admin@cloudmind.local / admin123")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
