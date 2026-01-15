from typing import List, Dict

class ExerciseLibrary:
    """Comprehensive exercise database organized by muscle groups"""
    
    def __init__(self):
        self.exercises = {
            "Chest": [
                {"name": "Barbell Bench Press", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "Incline Bench Press", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "Decline Bench Press", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "Dumbbell Bench Press", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Incline Dumbbell Press", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Dumbbell Flyes", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Cable Flyes", "equipment": "Cable", "difficulty": "Beginner"},
                {"name": "Push-Ups", "equipment": "Bodyweight", "difficulty": "Beginner"},
                {"name": "Chest Dips", "equipment": "Bodyweight", "difficulty": "Intermediate"},
                {"name": "Machine Chest Press", "equipment": "Machine", "difficulty": "Beginner"},
                {"name": "Pec Deck", "equipment": "Machine", "difficulty": "Beginner"},
            ],
            "Back": [
                {"name": "Deadlift", "equipment": "Barbell", "difficulty": "Advanced"},
                {"name": "Barbell Rows", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "T-Bar Rows", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "Dumbbell Rows", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Pull-Ups", "equipment": "Bodyweight", "difficulty": "Intermediate"},
                {"name": "Chin-Ups", "equipment": "Bodyweight", "difficulty": "Intermediate"},
                {"name": "Lat Pulldown", "equipment": "Cable", "difficulty": "Beginner"},
                {"name": "Seated Cable Rows", "equipment": "Cable", "difficulty": "Beginner"},
                {"name": "Face Pulls", "equipment": "Cable", "difficulty": "Beginner"},
                {"name": "Hyperextensions", "equipment": "Bodyweight", "difficulty": "Beginner"},
            ],
            "Shoulders": [
                {"name": "Overhead Press", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "Dumbbell Shoulder Press", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Arnold Press", "equipment": "Dumbbell", "difficulty": "Intermediate"},
                {"name": "Lateral Raises", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Front Raises", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Rear Delt Flyes", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Upright Rows", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "Cable Lateral Raises", "equipment": "Cable", "difficulty": "Beginner"},
                {"name": "Machine Shoulder Press", "equipment": "Machine", "difficulty": "Beginner"},
            ],
            "Legs": [
                {"name": "Barbell Squat", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "Front Squat", "equipment": "Barbell", "difficulty": "Advanced"},
                {"name": "Leg Press", "equipment": "Machine", "difficulty": "Beginner"},
                {"name": "Lunges", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Bulgarian Split Squats", "equipment": "Dumbbell", "difficulty": "Intermediate"},
                {"name": "Romanian Deadlift", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "Leg Extensions", "equipment": "Machine", "difficulty": "Beginner"},
                {"name": "Leg Curls", "equipment": "Machine", "difficulty": "Beginner"},
                {"name": "Calf Raises", "equipment": "Machine", "difficulty": "Beginner"},
                {"name": "Hack Squats", "equipment": "Machine", "difficulty": "Intermediate"},
            ],
            "Arms - Biceps": [
                {"name": "Barbell Curls", "equipment": "Barbell", "difficulty": "Beginner"},
                {"name": "Dumbbell Curls", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Hammer Curls", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Preacher Curls", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "Cable Curls", "equipment": "Cable", "difficulty": "Beginner"},
                {"name": "Concentration Curls", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "21s", "equipment": "Barbell", "difficulty": "Intermediate"},
            ],
            "Arms - Triceps": [
                {"name": "Close Grip Bench Press", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "Tricep Dips", "equipment": "Bodyweight", "difficulty": "Intermediate"},
                {"name": "Skull Crushers", "equipment": "Barbell", "difficulty": "Intermediate"},
                {"name": "Tricep Pushdowns", "equipment": "Cable", "difficulty": "Beginner"},
                {"name": "Overhead Tricep Extension", "equipment": "Dumbbell", "difficulty": "Beginner"},
                {"name": "Diamond Push-Ups", "equipment": "Bodyweight", "difficulty": "Intermediate"},
            ],
            "Core": [
                {"name": "Plank", "equipment": "Bodyweight", "difficulty": "Beginner"},
                {"name": "Side Plank", "equipment": "Bodyweight", "difficulty": "Beginner"},
                {"name": "Crunches", "equipment": "Bodyweight", "difficulty": "Beginner"},
                {"name": "Leg Raises", "equipment": "Bodyweight", "difficulty": "Intermediate"},
                {"name": "Russian Twists", "equipment": "Bodyweight", "difficulty": "Beginner"},
                {"name": "Ab Wheel Rollout", "equipment": "Ab Wheel", "difficulty": "Advanced"},
                {"name": "Cable Crunches", "equipment": "Cable", "difficulty": "Beginner"},
                {"name": "Hanging Leg Raises", "equipment": "Bodyweight", "difficulty": "Advanced"},
            ],
            "Cardio": [
                {"name": "Running", "equipment": "None", "difficulty": "Beginner"},
                {"name": "Treadmill", "equipment": "Machine", "difficulty": "Beginner"},
                {"name": "Cycling", "equipment": "Bike", "difficulty": "Beginner"},
                {"name": "Rowing", "equipment": "Machine", "difficulty": "Beginner"},
                {"name": "Elliptical", "equipment": "Machine", "difficulty": "Beginner"},
                {"name": "Jump Rope", "equipment": "Jump Rope", "difficulty": "Intermediate"},
                {"name": "Stair Climber", "equipment": "Machine", "difficulty": "Intermediate"},
                {"name": "Swimming", "equipment": "Pool", "difficulty": "Beginner"},
                {"name": "HIIT", "equipment": "None", "difficulty": "Advanced"},
            ],
        }
    
    def get_all_categories(self) -> List[str]:
        """Get list of all muscle group categories"""
        return list(self.exercises.keys())
    
    def get_exercises_by_category(self, category: str) -> List[Dict]:
        """Get all exercises for a specific category"""
        return self.exercises.get(category, [])
    
    def get_all_exercises(self) -> Dict:
        """Get complete exercise library"""
        return self.exercises
    
    def search_exercise(self, query: str) -> List[Dict]:
        """Search for exercises by name"""
        query_lower = query.lower()
        results = []
        
        for category, exercises in self.exercises.items():
            for exercise in exercises:
                if query_lower in exercise["name"].lower():
                    results.append({
                        **exercise,
                        "category": category
                    })
        
        return results
