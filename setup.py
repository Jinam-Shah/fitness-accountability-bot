#!/usr/bin/env python3
"""
Setup script for Fitness Accountability Bot
Initializes database and creates tables
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from backend.database.database import init_db

def main():
    print("=" * 60)
    print("🏋️  FITNESS ACCOUNTABILITY BOT - DATABASE SETUP")
    print("=" * 60)
    print()
    
    print("📦 Initializing database...")
    init_db()
    
    print("✅ Database created: fitness_app.db")
    print("✅ Tables created:")
    print("   - users")
    print("   - workouts")
    print("   - workout_programs")
    print("   - body_measurements")
    print()
    print("🎉 Setup complete! You can now run the application.")
    print()
    print("📝 Next steps:")
    print("   1. Start the API: uvicorn backend.api.main:app --reload")
    print("   2. Open frontend/index.html in your browser")
    print("   3. Register your account")
    print("   4. Start logging workouts!")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
