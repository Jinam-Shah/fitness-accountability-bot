from database import init_db, engine
from models import Base

def setup_database():
    print("=" * 60)
    print("🏋️  FITPRO ULTIMATE - DATABASE SETUP")
    print("=" * 60)
    print()
    
    print("📦 Initializing database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database created: fitness_app.db")
    print("✅ Tables created:")
    print("   - users")
    print("   - workouts")
    print("   - workout_programs")
    print("   - body_measurements")
    print("   - check_ins")
    print("   - personal_records")
    print("   - progress_photos")
    print("   - workout_templates")
    print()
    
    print("🎉 Setup complete! Your ultimate fitness platform is ready!")
    print()
    print("📝 Next steps:")
    print("   1. Start the API: uvicorn backend.api.main:app --reload")
    print("   2. Open frontend/index.html in your browser")
    print("   3. Register your account")
    print("   4. Start crushing your fitness goals! 💪")
    print()
    print("=" * 60)

if __name__ == "__main__":
    setup_database()
