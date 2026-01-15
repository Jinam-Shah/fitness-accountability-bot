import json
from typing import List, Dict
import random

class WorkoutGenerator:
    """Professional workout program generator with multiple plan templates"""
    
    def __init__(self):
        self.plan_templates = {
            "beginner_strength": {
                "name": "Beginner Full Body Strength",
                "description": "3-day full body routine for building foundational strength",
                "level": "beginner",
                "goal": "muscle_gain",
                "duration_weeks": 8,
                "days_per_week": 3,
                "schedule": [
                    {
                        "day": "Monday",
                        "focus": "Full Body A",
                        "exercises": [
                            {"name": "Squats", "sets": 3, "reps": 10, "rest": 90},
                            {"name": "Bench Press", "sets": 3, "reps": 10, "rest": 90},
                            {"name": "Barbell Rows", "sets": 3, "reps": 10, "rest": 90},
                            {"name": "Overhead Press", "sets": 3, "reps": 8, "rest": 90},
                            {"name": "Planks", "sets": 3, "reps": "30 sec", "rest": 60},
                        ]
                    },
                    {
                        "day": "Wednesday",
                        "focus": "Full Body B",
                        "exercises": [
                            {"name": "Deadlift", "sets": 3, "reps": 8, "rest": 120},
                            {"name": "Pull Ups", "sets": 3, "reps": 8, "rest": 90},
                            {"name": "Dumbbell Press", "sets": 3, "reps": 10, "rest": 90},
                            {"name": "Lunges", "sets": 3, "reps": 10, "rest": 60},
                            {"name": "Bicep Curls", "sets": 3, "reps": 12, "rest": 60},
                        ]
                    },
                    {
                        "day": "Friday",
                        "focus": "Full Body C",
                        "exercises": [
                            {"name": "Front Squats", "sets": 3, "reps": 10, "rest": 90},
                            {"name": "Incline Bench Press", "sets": 3, "reps": 10, "rest": 90},
                            {"name": "Cable Rows", "sets": 3, "reps": 12, "rest": 60},
                            {"name": "Lateral Raises", "sets": 3, "reps": 15, "rest": 60},
                            {"name": "Tricep Pushdowns", "sets": 3, "reps": 12, "rest": 60},
                        ]
                    }
                ]
            },
            
            "ppl_intermediate": {
                "name": "Push/Pull/Legs (PPL)",
                "description": "6-day split for intermediate lifters focusing on muscle growth",
                "level": "intermediate",
                "goal": "muscle_gain",
                "duration_weeks": 12,
                "days_per_week": 6,
                "schedule": [
                    {
                        "day": "Monday",
                        "focus": "Push (Chest, Shoulders, Triceps)",
                        "exercises": [
                            {"name": "Bench Press", "sets": 4, "reps": 8, "rest": 120},
                            {"name": "Overhead Press", "sets": 4, "reps": 8, "rest": 90},
                            {"name": "Incline Dumbbell Press", "sets": 3, "reps": 10, "rest": 90},
                            {"name": "Lateral Raises", "sets": 3, "reps": 15, "rest": 60},
                            {"name": "Tricep Dips", "sets": 3, "reps": 12, "rest": 60},
                            {"name": "Tricep Extensions", "sets": 3, "reps": 12, "rest": 60},
                        ]
                    },
                    {
                        "day": "Tuesday",
                        "focus": "Pull (Back, Biceps)",
                        "exercises": [
                            {"name": "Deadlift", "sets": 4, "reps": 6, "rest": 180},
                            {"name": "Pull Ups", "sets": 4, "reps": 8, "rest": 90},
                            {"name": "Barbell Rows", "sets": 4, "reps": 8, "rest": 90},
                            {"name": "Face Pulls", "sets": 3, "reps": 15, "rest": 60},
                            {"name": "Barbell Curls", "sets": 3, "reps": 10, "rest": 60},
                            {"name": "Hammer Curls", "sets": 3, "reps": 12, "rest": 60},
                        ]
                    },
                    {
                        "day": "Wednesday",
                        "focus": "Legs",
                        "exercises": [
                            {"name": "Squats", "sets": 4, "reps": 8, "rest": 180},
                            {"name": "Romanian Deadlift", "sets": 4, "reps": 10, "rest": 90},
                            {"name": "Leg Press", "sets": 3, "reps": 12, "rest": 90},
                            {"name": "Leg Curls", "sets": 3, "reps": 12, "rest": 60},
                            {"name": "Calf Raises", "sets": 4, "reps": 15, "rest": 60},
                        ]
                    },
                    {
                        "day": "Thursday",
                        "focus": "Push (Chest, Shoulders, Triceps)",
                        "exercises": [
                            {"name": "Incline Bench Press", "sets": 4, "reps": 8, "rest": 120},
                            {"name": "Dumbbell Shoulder Press", "sets": 4, "reps": 10, "rest": 90},
                            {"name": "Cable Flyes", "sets": 3, "reps": 12, "rest": 60},
                            {"name": "Front Raises", "sets": 3, "reps": 12, "rest": 60},
                            {"name": "Skull Crushers", "sets": 3, "reps": 10, "rest": 60},
                            {"name": "Tricep Pushdowns", "sets": 3, "reps": 15, "rest": 60},
                        ]
                    },
                    {
                        "day": "Friday",
                        "focus": "Pull (Back, Biceps)",
                        "exercises": [
                            {"name": "Lat Pulldown", "sets": 4, "reps": 10, "rest": 90},
                            {"name": "T-Bar Rows", "sets": 4, "reps": 10, "rest": 90},
                            {"name": "Dumbbell Rows", "sets": 3, "reps": 12, "rest": 60},
                            {"name": "Rear Delt Flyes", "sets": 3, "reps": 15, "rest": 60},
                            {"name": "Preacher Curls", "sets": 3, "reps": 12, "rest": 60},
                            {"name": "Cable Curls", "sets": 3, "reps": 15, "rest": 60},
                        ]
                    },
                    {
                        "day": "Saturday",
                        "focus": "Legs",
                        "exercises": [
                            {"name": "Front Squats", "sets": 4, "reps": 10, "rest": 120},
                            {"name": "Lunges", "sets": 3, "reps": 12, "rest": 90},
                            {"name": "Leg Extensions", "sets": 3, "reps": 15, "rest": 60},
                            {"name": "Leg Curls", "sets": 3, "reps": 15, "rest": 60},
                            {"name": "Seated Calf Raises", "sets": 4, "reps": 20, "rest": 60},
                        ]
                    }
                ]
            },
            
            "upper_lower": {
                "name": "Upper/Lower Split",
                "description": "4-day split alternating between upper and lower body",
                "level": "intermediate",
                "goal": "muscle_gain",
                "duration_weeks": 10,
                "days_per_week": 4,
                "schedule": [
                    {
                        "day": "Monday",
                        "focus": "Upper Body A",
                        "exercises": [
                            {"name": "Bench Press", "sets": 4, "reps": 6, "rest": 180},
                            {"name": "Barbell Rows", "sets": 4, "reps": 6, "rest": 180},
                            {"name": "Overhead Press", "sets": 3, "reps": 8, "rest": 90},
                            {"name": "Lat Pulldown", "sets": 3, "reps": 10, "rest": 90},
                            {"name": "Dumbbell Curls", "sets": 3, "reps": 12, "rest": 60},
                            {"name": "Tricep Dips", "sets": 3, "reps": 12, "rest": 60},
                        ]
                    },
                    {
                        "day": "Tuesday",
                        "focus": "Lower Body A",
                        "exercises": [
                            {"name": "Squats", "sets": 4, "reps": 6, "rest": 180},
                            {"name": "Romanian Deadlift", "sets": 3, "reps": 8, "rest": 120},
                            {"name": "Leg Press", "sets": 3, "reps": 12, "rest": 90},
                            {"name": "Leg Curls", "sets": 3, "reps": 12, "rest": 60},
                            {"name": "Calf Raises", "sets": 4, "reps": 15, "rest": 60},
                        ]
                    },
                    {
                        "day": "Thursday",
                        "focus": "Upper Body B",
                        "exercises": [
                            {"name": "Incline Bench Press", "sets": 4, "reps": 8, "rest": 120},
                            {"name": "Pull Ups", "sets": 4, "reps": 8, "rest": 90},
                            {"name": "Dumbbell Shoulder Press", "sets": 3, "reps": 10, "rest": 90},
                            {"name": "Cable Rows", "sets": 3, "reps": 12, "rest": 60},
                            {"name": "Lateral Raises", "sets": 3, "reps": 15, "rest": 60},
                            {"name": "Skull Crushers", "sets": 3, "reps": 12, "rest": 60},
                        ]
                    },
                    {
                        "day": "Friday",
                        "focus": "Lower Body B",
                        "exercises": [
                            {"name": "Deadlift", "sets": 4, "reps": 5, "rest": 180},
                            {"name": "Front Squats", "sets": 3, "reps": 8, "rest": 120},
                            {"name": "Lunges", "sets": 3, "reps": 12, "rest": 90},
                            {"name": "Leg Extensions", "sets": 3, "reps": 15, "rest": 60},
                            {"name": "Seated Calf Raises", "sets": 4, "reps": 20, "rest": 60},
                        ]
                    }
                ]
            },
            
            "fat_loss_circuit": {
                "name": "Fat Loss Circuit Training",
                "description": "High-intensity circuit training for maximum fat burning",
                "level": "intermediate",
                "goal": "weight_loss",
                "duration_weeks": 8,
                "days_per_week": 4,
                "schedule": [
                    {
                        "day": "Monday",
                        "focus": "Upper Body Circuit",
                        "exercises": [
                            {"name": "Push Ups", "sets": 4, "reps": 15, "rest": 30},
                            {"name": "Dumbbell Rows", "sets": 4, "reps": 12, "rest": 30},
                            {"name": "Dumbbell Press", "sets": 4, "reps": 12, "rest": 30},
                            {"name": "Battle Ropes", "sets": 4, "reps": "30 sec", "rest": 30},
                            {"name": "Burpees", "sets": 4, "reps": 10, "rest": 60},
                        ]
                    },
                    {
                        "day": "Tuesday",
                        "focus": "HIIT Cardio",
                        "exercises": [
                            {"name": "Running", "duration": 30, "intensity": "high", "calories": 400},
                            {"name": "Jump Rope", "sets": 5, "reps": "1 min", "rest": 60},
                        ]
                    },
                    {
                        "day": "Thursday",
                        "focus": "Lower Body Circuit",
                        "exercises": [
                            {"name": "Squats", "sets": 4, "reps": 20, "rest": 30},
                            {"name": "Lunges", "sets": 4, "reps": 15, "rest": 30},
                            {"name": "Box Jumps", "sets": 4, "reps": 10, "rest": 30},
                            {"name": "Mountain Climbers", "sets": 4, "reps": "30 sec", "rest": 30},
                            {"name": "Burpees", "sets": 4, "reps": 12, "rest": 60},
                        ]
                    },
                    {
                        "day": "Saturday",
                        "focus": "Full Body HIIT",
                        "exercises": [
                            {"name": "Kettlebell Swings", "sets": 4, "reps": 20, "rest": 30},
                            {"name": "Push Ups", "sets": 4, "reps": 15, "rest": 30},
                            {"name": "Jump Squats", "sets": 4, "reps": 15, "rest": 30},
                            {"name": "Mountain Climbers", "sets": 4, "reps": "45 sec", "rest": 30},
                            {"name": "Burpees", "sets": 4, "reps": 15, "rest": 90},
                        ]
                    }
                ]
            },
            
            "5x5_strength": {
                "name": "5x5 Strength Program",
                "description": "Classic strength building program for advanced lifters",
                "level": "advanced",
                "goal": "muscle_gain",
                "duration_weeks": 12,
                "days_per_week": 3,
                "schedule": [
                    {
                        "day": "Monday",
                        "focus": "Workout A",
                        "exercises": [
                            {"name": "Squats", "sets": 5, "reps": 5, "rest": 180},
                            {"name": "Bench Press", "sets": 5, "reps": 5, "rest": 180},
                            {"name": "Barbell Rows", "sets": 5, "reps": 5, "rest": 180},
                        ]
                    },
                    {
                        "day": "Wednesday",
                        "focus": "Workout B",
                        "exercises": [
                            {"name": "Squats", "sets": 5, "reps": 5, "rest": 180},
                            {"name": "Overhead Press", "sets": 5, "reps": 5, "rest": 180},
                            {"name": "Deadlift", "sets": 1, "reps": 5, "rest": 180},
                        ]
                    },
                    {
                        "day": "Friday",
                        "focus": "Workout A",
                        "exercises": [
                            {"name": "Squats", "sets": 5, "reps": 5, "rest": 180},
                            {"name": "Bench Press", "sets": 5, "reps": 5, "rest": 180},
                            {"name": "Barbell Rows", "sets": 5, "reps": 5, "rest": 180},
                        ]
                    }
                ]
            }
        }
    
    def get_available_plans(self) -> List[Dict]:
        """Get list of all available workout plans"""
        plans = []
        for plan_id, plan_data in self.plan_templates.items():
            plans.append({
                "id": plan_id,
                "name": plan_data["name"],
                "description": plan_data["description"],
                "level": plan_data["level"],
                "goal": plan_data["goal"],
                "duration_weeks": plan_data["duration_weeks"],
                "days_per_week": plan_data["days_per_week"]
            })
        return plans
    
    def get_plan_by_id(self, plan_id: str) -> Dict:
        """Get specific plan by ID"""
        return self.plan_templates.get(plan_id)
    
    def calculate_bmi(self, weight_kg: float, height_cm: float) -> float:
        """Calculate Body Mass Index"""
        height_m = height_cm / 100
        return round(weight_kg / (height_m ** 2), 2)
    
    def calculate_bmr(self, weight_kg: float, height_cm: float, age: int, gender: str) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == "male":
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        return round(bmr, 2)
    
    def calculate_daily_calories(self, bmr: float, activity_level: str, goal: str) -> int:
        """Calculate daily calorie target based on activity and goals"""
        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        
        maintenance = bmr * activity_multipliers.get(activity_level, 1.55)
        
        if goal == "weight_loss":
            return int(maintenance - 500)
        elif goal == "muscle_gain":
            return int(maintenance + 300)
        else:
            return int(maintenance)
    
    def estimate_calories_burned(self, exercise_name: str, sets: int = None, 
                                reps: int = None, duration_minutes: int = None, 
                                weight_kg: float = None) -> int:
        """Estimate calories burned for an exercise"""
        
        # Cardio exercises (per minute)
        cardio_rates = {
            "running": 12, "cycling": 9, "swimming": 11,
            "walking": 5, "rowing": 10, "elliptical": 8,
            "hiit": 15, "jump rope": 13, "burpees": 10
        }
        
        # Check if cardio
        for cardio_ex, rate in cardio_rates.items():
            if cardio_ex in exercise_name.lower():
                if duration_minutes:
                    return int(duration_minutes * rate)
                return 100  # Default
        
        # Strength training estimation
        if sets and reps:
            base = sets * reps * 2.5
            if weight_kg:
                base += weight_kg * 0.5
            return int(base)
        
        return 50  # Minimum default

# Test
if __name__ == "__main__":
    gen = WorkoutGenerator()
    plans = gen.get_available_plans()
    print("📋 Available Plans:\n")
    for plan in plans:
        print(f"✅ {plan['name']}")
        print(f"   Level: {plan['level']} | Goal: {plan['goal']} | {plan['days_per_week']} days/week")
        print(f"   {plan['description']}\n")
