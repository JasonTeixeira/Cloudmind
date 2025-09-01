#!/usr/bin/env python3
"""
Development Startup Script for CloudMind
Phase 1: Foundation Fixes
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_development_config():
    """Load development configuration"""
    try:
        # Import and execute the development config
        import config_dev
        logger.info("✅ Development configuration loaded")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to load development config: {e}")
        return False


def initialize_database():
    """Initialize the database"""
    try:
        # Run the database initialization script
        result = subprocess.run([
            sys.executable, "scripts/init_database.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ Database initialized successfully")
            return True
        else:
            logger.error(f"❌ Database initialization failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        return False


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import sqlalchemy
        import uvicorn
        import redis
        logger.info("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        logger.error(f"❌ Missing dependency: {e}")
        logger.info("📦 Install dependencies with: pip install -r requirements.txt")
        return False


def create_directories():
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
        
        logger.info("✅ Directories created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to create directories: {e}")
        return False


def start_server():
    """Start the development server"""
    try:
        logger.info("🚀 Starting CloudMind development server...")
        logger.info("📋 Server will be available at: http://localhost:8000")
        logger.info("📋 API docs will be available at: http://localhost:8000/docs")
        logger.info("📋 Press Ctrl+C to stop the server")
        
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ])
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")


def main():
    """Main startup function"""
    logger.info("🚀 CloudMind Development Startup")
    logger.info("=" * 50)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        return False
    
    # Step 2: Load development configuration
    if not load_development_config():
        return False
    
    # Step 3: Create directories
    if not create_directories():
        return False
    
    # Step 4: Initialize database
    if not initialize_database():
        return False
    
    # Step 5: Start server
    start_server()
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
