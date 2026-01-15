from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from typing import List, Optional
from pydantic import BaseModel, EmailStr
import json
import base64

from backend.database.database import get_db, init_db
from backend.database.models import (
    User, Workout, WorkoutProgram, BodyMeasurement, 
    CheckIn, PersonalRecord, ProgressPhoto, WorkoutTemplate
)
from backend.api.auth import get_password_hash, verify_password, create_access_token, get_current_user
from backend.services.workout_generator import WorkoutGenerator
from backend.services.nlp_engine import SmartFitnessNLP
from backend.services.exercise_library import ExerciseLibrary

# Initialize FastAPI
app = FastAPI(
    title="FitPro - Ultimate Fitness Platform",
    description="Complete fitness ecosystem with custom plans, calendar, and tracking",
    version="5.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
workout_gen = WorkoutGenerator()
nlp_engine = SmartFitnessNLP()
exercise_lib = ExerciseLibrary()

# ==================== PYDANTIC MODELS ====================

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    fitness_level: str
    fitness_goal: str
    target_weight_kg: Optional[float] = None
    selected_plan: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class WorkoutLog(BaseModel):
    message: str

class ManualWorkoutLog(BaseModel):
    exercise_name: str
    category: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight_kg: Optional[float] = None
    duration_minutes: Optional[int] = None
    distance_km: Optional[float] = None
    notes: Optional[str] = None
    feeling: Optional[str] = None

class CheckInCreate(BaseModel):
    check_in_date: str  # YYYY-MM-DD
    workout_completed: bool
    notes: Optional[str] = None

class CustomProgramCreate(BaseModel):
    program_name: str
    duration_weeks: int
    days_per_week: int
    schedule: List[dict]  # Array of workout days

class WorkoutTemplateCreate(BaseModel):
    template_name: str
    exercises: List[dict]

class PersonalRecordCreate(BaseModel):
    exercise_name: str
    record_type: str
    value: float
    unit: str

class ProgressPhotoCreate(BaseModel):
    photo_base64: str
    weight_kg: Optional[float] = None
    notes: Optional[str] = None

# Database initialization
@app.on_event("startup")
def on_startup():
    init_db()
    print("✅ FitPro Ultimate API Ready! 🚀")

@app.get("/")
def root():
    return {
        "app": "FitPro - Ultimate Fitness Platform",
        "version": "5.0.0",
        "features": [
            "✅ Custom Workout Plan Builder",
            "✅ Exercise Library (100+ exercises)",
            "✅ Calendar & Check-ins",
            "✅ Manual Exercise Logger",
            "✅ Progress Photos",
            "✅ Personal Records Tracking",
            "✅ Workout Templates",
            "✅ Streak Tracking",
            "✅ Advanced NLP",
        ]
    }

# ==================== EXERCISE LIBRARY ====================

@app.get("/exercises/categories")
def get_exercise_categories():
    """Get all exercise categories"""
    categories = exercise_lib.get_all_categories()
    return {"categories": categories}

@app.get("/exercises/category/{category}")
def get_exercises_by_category(category: str):
    """Get exercises for a specific category"""
    exercises = exercise_lib.get_exercises_by_category(category)
    if not exercises:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"category": category, "exercises": exercises}

@app.get("/exercises/all")
def get_all_exercises():
    """Get complete exercise library"""
    return exercise_lib.get_all_exercises()

@app.get("/exercises/search/{query}")
def search_exercises(query: str):
    """Search exercises by name"""
    results = exercise_lib.search_exercise(query)
    return {"results": results, "count": len(results)}

# ==================== WORKOUT PLANS ====================

@app.get("/plans/available")
def get_available_plans():
    """Get all available workout plan templates"""
    plans = workout_gen.get_available_plans()
    return {"plans": plans, "total": len(plans)}

@app.get("/plans/{plan_id}")
def get_plan_details(plan_id: str):
    """Get detailed information about a specific plan"""
    plan = workout_gen.get_plan_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

# ==================== AUTHENTICATION ====================

@app.post("/register")
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register new user"""
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    bmi = workout_gen.calculate_bmi(user_data.weight_kg, user_data.height_cm)
    bmr = workout_gen.calculate_bmr(user_data.weight_kg, user_data.height_cm, user_data.age, user_data.gender)
    daily_calories = workout_gen.calculate_daily_calories(bmr, "moderate", user_data.fitness_goal)
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        age=user_data.age,
        gender=user_data.gender,
        height_cm=user_data.height_cm,
        weight_kg=user_data.weight_kg,
        fitness_level=user_data.fitness_level,
        fitness_goal=user_data.fitness_goal,
        target_weight_kg=user_data.target_weight_kg,
        bmi=bmi,
        bmr=bmr,
        daily_calorie_target=daily_calories
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create program
    if user_data.selected_plan:
        plan_template = workout_gen.get_plan_by_id(user_data.selected_plan)
    else:
        default_plans = {"beginner": "beginner_strength", "intermediate": "ppl_intermediate", "advanced": "5x5_strength"}
        plan_id = default_plans.get(user_data.fitness_level, "beginner_strength")
        plan_template = workout_gen.get_plan_by_id(plan_id)
    
    new_program = WorkoutProgram(
        user_id=new_user.id,
        program_name=plan_template["name"],
        program_type=user_data.selected_plan or "default",
        duration_weeks=plan_template["duration_weeks"],
        days_per_week=plan_template["days_per_week"],
        exercises=json.dumps(plan_template["schedule"])
    )
    
    db.add(new_program)
    db.commit()
    
    access_token = create_access_token(data={"sub": new_user.email})
    
    return {
        "message": f"Welcome to FitPro! Your {new_program.program_name} is ready!",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username,
            "full_name": new_user.full_name
        }
    }

@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """User login"""
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name
        }
    }

# ==================== PROFILE ====================

@app.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "age": current_user.age,
        "gender": current_user.gender,
        "height_cm": current_user.height_cm,
        "weight_kg": current_user.weight_kg,
        "fitness_level": current_user.fitness_level,
        "fitness_goal": current_user.fitness_goal,
        "target_weight_kg": current_user.target_weight_kg,
        "bmi": current_user.bmi,
        "bmr": current_user.bmr,
        "daily_calorie_target": current_user.daily_calorie_target,
        "current_streak": current_user.current_streak,
        "longest_streak": current_user.longest_streak,
        "total_workouts": current_user.total_workouts,
        "created_at": current_user.created_at
    }

# ==================== WORKOUT LOGGING ====================

@app.post("/workouts/log/nlp")
def log_workout_nlp(
    workout_data: WorkoutLog,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log workout using NLP"""
    message = workout_data.message.lower()
    
    # Special commands
    if "stats" in message or "progress" in message:
        all_workouts = db.query(Workout).filter(Workout.user_id == current_user.id).all()
        response = f"📊 Your Stats:\n🏋️ Total: {len(all_workouts)} workouts\n🔥 Calories: {sum(w.calories_burned for w in all_workouts)}"
        return {"success": True, "message": response, "stats": True}
    
    parsed = nlp_engine.parse_workout(workout_data.message)
    
    if not parsed:
        return {
            "success": False,
            "message": "❌ Couldn't understand. Try: 'bench press 4x8 at 80kg' or use manual logger"
        }
    
    calories = workout_gen.estimate_calories_burned(
        parsed["exercise_name"],
        parsed.get("sets"),
        parsed.get("reps"),
        parsed.get("duration_minutes"),
        parsed.get("weight_kg")
    )
    
    new_workout = Workout(
        user_id=current_user.id,
        workout_type=parsed["workout_type"],
        exercise_name=parsed["exercise_name"],
        sets=parsed.get("sets"),
        reps=parsed.get("reps"),
        weight_kg=parsed.get("weight_kg"),
        duration_minutes=parsed.get("duration_minutes"),
        distance_km=parsed.get("distance_km"),
        calories_burned=calories,
        intensity="moderate",
        notes=workout_data.message
    )
    
    db.add(new_workout)
    current_user.total_workouts += 1
    db.commit()
    
    response = f"✅ Logged: {parsed['exercise_name'].title()}\n"
    if parsed.get("sets"): response += f"💪 {parsed['sets']}×{parsed['reps']}\n"
    if parsed.get("weight_kg"): response += f"⚖️ {parsed['weight_kg']}kg\n"
    response += f"🔥 ~{calories} cal"
    
    return {"success": True, "message": response, "workout_id": new_workout.id}

@app.post("/workouts/log/manual")
def log_workout_manual(
    workout_data: ManualWorkoutLog,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log workout manually with all details"""
    
    workout_type = "cardio" if workout_data.category == "Cardio" else "strength"
    
    calories = workout_gen.estimate_calories_burned(
        workout_data.exercise_name,
        workout_data.sets,
        workout_data.reps,
        workout_data.duration_minutes,
        workout_data.weight_kg
    )
    
    new_workout = Workout(
        user_id=current_user.id,
        workout_type=workout_type,
        exercise_name=workout_data.exercise_name,
        sets=workout_data.sets,
        reps=workout_data.reps,
        weight_kg=workout_data.weight_kg,
        duration_minutes=workout_data.duration_minutes,
        distance_km=workout_data.distance_km,
        calories_burned=calories,
        notes=workout_data.notes,
        feeling=workout_data.feeling
    )
    
    db.add(new_workout)
    current_user.total_workouts += 1
    
    # Check for Personal Record
    if workout_data.weight_kg and workout_data.sets and workout_data.reps:
        existing_pr = db.query(PersonalRecord).filter(
            PersonalRecord.user_id == current_user.id,
            PersonalRecord.exercise_name == workout_data.exercise_name,
            PersonalRecord.record_type == "max_weight"
        ).first()
        
        if not existing_pr or workout_data.weight_kg > existing_pr.value:
            if existing_pr:
                existing_pr.value = workout_data.weight_kg
                existing_pr.achieved_at = datetime.utcnow()
            else:
                new_pr = PersonalRecord(
                    user_id=current_user.id,
                    exercise_name=workout_data.exercise_name,
                    record_type="max_weight",
                    value=workout_data.weight_kg,
                    unit="kg"
                )
                db.add(new_pr)
    
    db.commit()
    
    return {
        "message": "✅ Workout logged successfully!",
        "workout_id": new_workout.id,
        "calories": calories
    }

@app.get("/workouts/history")
def get_workout_history(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workout history"""
    start_date = datetime.now() - timedelta(days=days)
    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.logged_at >= start_date
    ).order_by(Workout.logged_at.desc()).all()
    
    return {
        "workouts": [
            {
                "id": w.id,
                "exercise_name": w.exercise_name,
                "workout_type": w.workout_type,
                "sets": w.sets,
                "reps": w.reps,
                "weight_kg": w.weight_kg,
                "duration_minutes": w.duration_minutes,
                "distance_km": w.distance_km,
                "calories_burned": w.calories_burned,
                "feeling": w.feeling,
                "logged_at": w.logged_at.isoformat(),
                "notes": w.notes
            } for w in workouts
        ]
    }

@app.delete("/workouts/{workout_id}")
def delete_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a workout"""
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()
    
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    db.delete(workout)
    current_user.total_workouts = max(0, current_user.total_workouts - 1)
    db.commit()
    
    return {"message": "Workout deleted"}

# ==================== CALENDAR & CHECK-INS ====================

@app.post("/checkin")
def create_checkin(
    checkin_data: CheckInCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a check-in for a specific date"""
    checkin_date = datetime.strptime(checkin_data.check_in_date, "%Y-%m-%d").date()
    
    # Check if already exists
    existing = db.query(CheckIn).filter(
        CheckIn.user_id == current_user.id,
        CheckIn.check_in_date == checkin_date
    ).first()
    
    if existing:
        existing.workout_completed = checkin_data.workout_completed
        existing.notes = checkin_data.notes
    else:
        new_checkin = CheckIn(
            user_id=current_user.id,
            check_in_date=checkin_date,
            workout_completed=checkin_data.workout_completed,
            notes=checkin_data.notes
        )
        db.add(new_checkin)
    
    # Update streak
    update_streak(current_user, db)
    
    db.commit()
    
    return {"message": "Check-in recorded!", "streak": current_user.current_streak}

@app.get("/checkins/month/{year}/{month}")
def get_month_checkins(
    year: int,
    month: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all check-ins for a specific month"""
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    
    checkins = db.query(CheckIn).filter(
        CheckIn.user_id == current_user.id,
        CheckIn.check_in_date >= start_date,
        CheckIn.check_in_date < end_date
    ).all()
    
    # Also get workouts for the month
    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.workout_date >= start_date,
        Workout.workout_date < end_date
    ).all()
    
    # Create calendar data
    calendar_data = {}
    for checkin in checkins:
        date_str = checkin.check_in_date.isoformat()
        calendar_data[date_str] = {
            "checked_in": True,
            "workout_completed": checkin.workout_completed,
            "notes": checkin.notes
        }
    
    for workout in workouts:
        date_str = workout.workout_date.isoformat()
        if date_str not in calendar_data:
            calendar_data[date_str] = {"checked_in": False, "workout_completed": True}
        calendar_data[date_str]["workout_count"] = calendar_data[date_str].get("workout_count", 0) + 1
    
    return {"calendar": calendar_data, "current_streak": current_user.current_streak}

def update_streak(user: User, db: Session):
    """Update user's workout streak"""
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    today_checkin = db.query(CheckIn).filter(
        CheckIn.user_id == user.id,
        CheckIn.check_in_date == today,
        CheckIn.workout_completed == True
    ).first()
    
    yesterday_checkin = db.query(CheckIn).filter(
        CheckIn.user_id == user.id,
        CheckIn.check_in_date == yesterday,
        CheckIn.workout_completed == True
    ).first()
    
    if today_checkin:
        if yesterday_checkin or user.current_streak == 0:
            user.current_streak += 1
        if user.current_streak > user.longest_streak:
            user.longest_streak = user.current_streak
    elif not yesterday_checkin:
        user.current_streak = 0

# ==================== CUSTOM PROGRAMS ====================

@app.post("/programs/custom")
def create_custom_program(
    program_data: CustomProgramCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a custom workout program"""
    
    # Deactivate current programs
    db.query(WorkoutProgram).filter(
        WorkoutProgram.user_id == current_user.id
    ).update({"is_active": False})
    
    new_program = WorkoutProgram(
        user_id=current_user.id,
        program_name=program_data.program_name,
        program_type="custom",
        duration_weeks=program_data.duration_weeks,
        days_per_week=program_data.days_per_week,
        exercises=json.dumps(program_data.schedule)
    )
    
    db.add(new_program)
    db.commit()
    
    return {"message": f"Custom program '{program_data.program_name}' created!", "program_id": new_program.id}

@app.get("/programs/my")
def get_my_programs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user programs"""
    programs = db.query(WorkoutProgram).filter(
        WorkoutProgram.user_id == current_user.id
    ).all()
    
    return {
        "programs": [
            {
                "id": p.id,
                "name": p.program_name,
                "type": p.program_type,
                "weeks": p.duration_weeks,
                "days_per_week": p.days_per_week,
                "is_active": p.is_active
            } for p in programs
        ]
    }

@app.post("/programs/{program_id}/activate")
def activate_program(
    program_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Activate a specific program"""
    # Deactivate all
    db.query(WorkoutProgram).filter(
        WorkoutProgram.user_id == current_user.id
    ).update({"is_active": False})
    
    # Activate selected
    program = db.query(WorkoutProgram).filter(
        WorkoutProgram.id == program_id,
        WorkoutProgram.user_id == current_user.id
    ).first()
    
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    program.is_active = True
    db.commit()
    
    return {"message": f"Program '{program.program_name}' activated!"}

@app.get("/programs/active")
def get_active_program(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get active program"""
    program = db.query(WorkoutProgram).filter(
        WorkoutProgram.user_id == current_user.id,
        WorkoutProgram.is_active == True
    ).first()
    
    if not program:
        return {"message": "No active program"}
    
    return {
        "program_name": program.program_name,
        "schedule": json.loads(program.exercises)
    }

# ==================== WORKOUT TEMPLATES ====================

@app.post("/templates")
def create_template(
    template_data: WorkoutTemplateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create workout template"""
    new_template = WorkoutTemplate(
        user_id=current_user.id,
        template_name=template_data.template_name,
        exercises=json.dumps(template_data.exercises)
    )
    
    db.add(new_template)
    db.commit()
    
    return {"message": "Template saved!", "template_id": new_template.id}

@app.get("/templates")
def get_templates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all user templates"""
    templates = db.query(WorkoutTemplate).filter(
        WorkoutTemplate.user_id == current_user.id
    ).all()
    
    return {
        "templates": [
            {
                "id": t.id,
                "name": t.template_name,
                "exercises": json.loads(t.exercises)
            } for t in templates
        ]
    }

# ==================== PERSONAL RECORDS ====================

@app.get("/records")
def get_personal_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all personal records"""
    records = db.query(PersonalRecord).filter(
        PersonalRecord.user_id == current_user.id
    ).order_by(PersonalRecord.achieved_at.desc()).all()
    
    return {
        "records": [
            {
                "exercise": r.exercise_name,
                "type": r.record_type,
                "value": r.value,
                "unit": r.unit,
                "date": r.achieved_at.isoformat()
            } for r in records
        ]
    }

# ==================== PROGRESS PHOTOS ====================

@app.post("/photos")
def upload_progress_photo(
    photo_data: ProgressPhotoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload progress photo"""
    new_photo = ProgressPhoto(
        user_id=current_user.id,
        photo_url=photo_data.photo_base64,
        weight_kg=photo_data.weight_kg,
        notes=photo_data.notes
    )
    
    db.add(new_photo)
    db.commit()
    
    return {"message": "Photo uploaded!", "photo_id": new_photo.id}

@app.get("/photos")
def get_progress_photos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all progress photos"""
    photos = db.query(ProgressPhoto).filter(
        ProgressPhoto.user_id == current_user.id
    ).order_by(ProgressPhoto.taken_at.desc()).all()
    
    return {
        "photos": [
            {
                "id": p.id,
                "photo": p.photo_url,
                "weight": p.weight_kg,
                "notes": p.notes,
                "date": p.taken_at.isoformat()
            } for p in photos
        ]
    }

# ==================== STATISTICS ====================

@app.get("/stats/overview")
def get_stats_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get complete statistics"""
    all_workouts = db.query(Workout).filter(Workout.user_id == current_user.id).all()
    
    week_start = datetime.now() - timedelta(days=datetime.now().weekday())
    week_workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.logged_at >= week_start
    ).all()
    
    return {
        "all_time": {
            "total_workouts": len(all_workouts),
            "total_calories": sum(w.calories_burned for w in all_workouts),
            "total_minutes": sum(w.duration_minutes or 0 for w in all_workouts),
        },
        "this_week": {
            "workouts": len(week_workouts),
            "calories": sum(w.calories_burned for w in week_workouts),
            "minutes": sum(w.duration_minutes or 0 for w in week_workouts),
        },
        "streaks": {
            "current": current_user.current_streak,
            "longest": current_user.longest_streak
        },
        "user_metrics": {
            "current_weight": current_user.weight_kg,
            "target_weight": current_user.target_weight_kg,
            "bmi": current_user.bmi,
            "daily_calorie_target": current_user.daily_calorie_target
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
