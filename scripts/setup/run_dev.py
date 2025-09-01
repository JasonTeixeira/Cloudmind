#!/usr/bin/env python3
"""
Simple Development Startup for CloudMind
Phase 1: Foundation Fixes
"""

import os
import sys
import subprocess

def setup_environment():
    """Set up development environment"""
    print("🔧 Setting up development environment...")
    
    # Import and run environment setup
    import setup_env
    setup_env.setup_development_environment()
    
    print("✅ Environment setup complete")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    import os
    directories = [
        "./storage",
        "./git-repos", 
        "./templates",
        "./backups",
        "./logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")

def initialize_database():
    """Initialize database"""
    print("🗄️ Initializing database...")
    
    try:
        from app.core.database import Base, engine
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def start_server():
    """Start the development server"""
    print("\n🚀 Starting CloudMind development server...")
    print("📋 Server will be available at: http://localhost:8000")
    print("📋 API docs will be available at: http://localhost:8000/docs")
    print("📋 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    """Main startup function"""
    print("🚀 CloudMind Development Startup")
    print("=" * 50)
    
    # Step 1: Setup environment
    setup_environment()
    
    # Step 2: Create directories
    create_directories()
    
    # Step 3: Initialize database
    if not initialize_database():
        print("❌ Failed to initialize database")
        return False
    
    # Step 4: Start server
    start_server()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
