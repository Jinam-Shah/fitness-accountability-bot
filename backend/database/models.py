from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Profile Information
    full_name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    
    # Fitness Profile
    fitness_level = Column(String, default="beginner")
    fitness_goal = Column(String)
    target_weight_kg = Column(Float, nullable=True)
    
    # Health Metrics
    bmi = Column(Float, nullable=True)
    bmr = Column(Float, nullable=True)
    daily_calorie_target = Column(Integer, nullable=True)
    
    # Streak & Engagement
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    total_workouts = Column(Integer, default=0)
    
    # Account Info
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    programs = relationship("WorkoutProgram", back_populates="user", cascade="all, delete-orphan")
    body_measurements = relationship("BodyMeasurement", back_populates="user", cascade="all, delete-orphan")
    check_ins = relationship("CheckIn", back_populates="user", cascade="all, delete-orphan")
    personal_records = relationship("PersonalRecord", back_populates="user", cascade="all, delete-orphan")
    progress_photos = relationship("ProgressPhoto", back_populates="user", cascade="all, delete-orphan")
    workout_templates = relationship("WorkoutTemplate", back_populates="user", cascade="all, delete-orphan")

class Workout(Base):
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Workout Details
    workout_type = Column(String)
    exercise_name = Column(String, nullable=False)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    weight_kg = Column(Float, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    distance_km = Column(Float, nullable=True)
    
    # Metrics
    calories_burned = Column(Integer)
    intensity = Column(String)
    
    # Notes
    notes = Column(Text, nullable=True)
    feeling = Column(String, nullable=True)
    
    # Timestamp
    logged_at = Column(DateTime, default=datetime.utcnow)
    workout_date = Column(Date, default=datetime.utcnow)
    
    user = relationship("User", back_populates="workouts")

class WorkoutProgram(Base):
    __tablename__ = "workout_programs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    program_name = Column(String, nullable=False)
    program_type = Column(String)  # template or custom
    duration_weeks = Column(Integer)
    days_per_week = Column(Integer)
    
    # Program Details (JSON stored as text)
    exercises = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="programs")

class BodyMeasurement(Base):
    __tablename__ = "body_measurements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    weight_kg = Column(Float, nullable=False)
    body_fat_percentage = Column(Float, nullable=True)
    chest_cm = Column(Float, nullable=True)
    waist_cm = Column(Float, nullable=True)
    hips_cm = Column(Float, nullable=True)
    biceps_cm = Column(Float, nullable=True)
    thighs_cm = Column(Float, nullable=True)
    
    measured_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="body_measurements")

class CheckIn(Base):
    __tablename__ = "check_ins"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    check_in_date = Column(Date, nullable=False)
    workout_completed = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="check_ins")

class PersonalRecord(Base):
    __tablename__ = "personal_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    exercise_name = Column(String, nullable=False)
    record_type = Column(String)  # max_weight, max_reps, max_distance
    value = Column(Float, nullable=False)
    unit = Column(String)  # kg, reps, km
    
    achieved_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="personal_records")

class ProgressPhoto(Base):
    __tablename__ = "progress_photos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    photo_url = Column(String)  # Base64 or file path
    weight_kg = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    
    taken_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="progress_photos")

class WorkoutTemplate(Base):
    __tablename__ = "workout_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    template_name = Column(String, nullable=False)
    exercises = Column(Text)  # JSON array of exercises
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="workout_templates")
