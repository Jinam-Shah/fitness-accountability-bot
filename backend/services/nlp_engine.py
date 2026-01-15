import re
from typing import Dict, Optional, List

class SmartFitnessNLP:
    """Advanced NLP for natural workout logging with comprehensive exercise database"""
    
    def __init__(self):
        # Comprehensive exercise database with variations
        self.exercise_database = {
            # CHEST
            "bench press": ["bench", "bench press", "barbell bench", "flat bench"],
            "incline bench press": ["incline bench", "incline press"],
            "decline bench press": ["decline bench", "decline press"],
            "chest press": ["chest press", "machine chest press", "chest machine"],
            "dumbbell press": ["dumbbell press", "db press", "dumbell press"],
            "push ups": ["pushup", "push up", "push-up", "pushups", "press up"],
            "cable flyes": ["cable fly", "cable flyes", "chest fly"],
            "dumbbell flyes": ["dumbbell fly", "db fly", "dumbell fly"],
            "chest dips": ["chest dip", "dips"],
            
            # BACK
            "deadlift": ["deadlift", "deadlifts", "dead lift"],
            "barbell rows": ["barbell row", "bb row", "bent over row"],
            "dumbbell rows": ["dumbbell row", "db row", "one arm row"],
            "pull ups": ["pullup", "pull up", "pull-up", "pullups", "chin up"],
            "lat pulldown": ["lat pull down", "lat pulldown", "pulldown"],
            "cable rows": ["cable row", "seated cable row", "seated row"],
            "t-bar rows": ["t-bar row", "t bar row"],
            "face pulls": ["face pull"],
            
            # SHOULDERS
            "overhead press": ["overhead press", "ohp", "shoulder press", "military press"],
            "dumbbell shoulder press": ["db shoulder press", "dumbbell press"],
            "lateral raises": ["lateral raise", "side raise", "side lateral"],
            "front raises": ["front raise"],
            "rear delt flyes": ["rear delt", "reverse fly", "rear fly"],
            "arnold press": ["arnold", "arnold press"],
            "upright rows": ["upright row"],
            
            # LEGS
            "squats": ["squat", "squats", "back squat", "barbell squat"],
            "front squats": ["front squat"],
            "leg press": ["leg press"],
            "lunges": ["lunge", "walking lunge"],
            "leg extensions": ["leg extension"],
            "leg curls": ["leg curl", "hamstring curl"],
            "romanian deadlift": ["rdl", "romanian deadlift", "romanian"],
            "calf raises": ["calf raise", "standing calf"],
            "hack squats": ["hack squat"],
            
            # ARMS
            "bicep curls": ["bicep curl", "barbell curl", "curl", "curls"],
            "dumbbell curls": ["dumbbell curl", "db curl", "alternating curl"],
            "hammer curls": ["hammer curl"],
            "preacher curls": ["preacher curl"],
            "tricep extensions": ["tricep extension", "overhead extension"],
            "tricep pushdowns": ["tricep pushdown", "cable pushdown", "pushdown"],
            "tricep dips": ["tricep dip", "bench dip"],
            "skull crushers": ["skull crusher", "lying tricep extension"],
            "close grip bench": ["close grip bench", "close grip"],
            
            # CORE
            "planks": ["plank", "front plank"],
            "side planks": ["side plank"],
            "crunches": ["crunch", "abdominal crunch"],
            "sit ups": ["situp", "sit up", "sit-up"],
            "leg raises": ["leg raise", "hanging leg raise"],
            "russian twists": ["russian twist"],
            "mountain climbers": ["mountain climber"],
            "ab wheel": ["ab wheel", "rollout"],
            
            # CARDIO
            "running": ["run", "running", "ran", "jog", "jogging"],
            "treadmill": ["treadmill"],
            "cycling": ["cycle", "cycling", "cycled", "bike", "biking"],
            "swimming": ["swim", "swimming", "swam"],
            "walking": ["walk", "walking", "walked"],
            "rowing": ["row", "rowing", "rower"],
            "elliptical": ["elliptical"],
            "stair climber": ["stairmaster", "stair climber", "stairs"],
            "jump rope": ["jump rope", "skipping", "rope"],
            "burpees": ["burpee"],
            
            # HIIT/FUNCTIONAL
            "hiit": ["hiit", "high intensity", "interval training"],
            "box jumps": ["box jump"],
            "battle ropes": ["battle rope"],
            "kettlebell swings": ["kettlebell swing", "kb swing"],
            "wall balls": ["wall ball"],
            
            # FLEXIBILITY
            "yoga": ["yoga"],
            "stretching": ["stretch", "stretching"],
            "pilates": ["pilates"],
        }
        
        # Create reverse lookup
        self.exercise_lookup = {}
        for standard_name, variations in self.exercise_database.items():
            for variation in variations:
                self.exercise_lookup[variation.lower()] = standard_name
    
    def find_exercise(self, text: str) -> Optional[str]:
        """Find exercise name in text using fuzzy matching"""
        text_lower = text.lower()
        
        # Direct match
        for variation, standard_name in self.exercise_lookup.items():
            if variation in text_lower:
                return standard_name
        
        # Partial word match
        words = text_lower.split()
        for i in range(len(words)):
            for j in range(i + 1, len(words) + 1):
                phrase = " ".join(words[i:j])
                if phrase in self.exercise_lookup:
                    return self.exercise_lookup[phrase]
        
        return None
    
    def parse_workout(self, text: str) -> Optional[Dict]:
        """Parse natural language workout input with enhanced flexibility"""
        text_lower = text.lower()
        result = {}
        
        # Find exercise
        exercise = self.find_exercise(text)
        if not exercise:
            return None
        
        result["exercise_name"] = exercise
        
        # Determine workout type
        cardio_exercises = ["running", "cycling", "swimming", "walking", "rowing", 
                          "elliptical", "treadmill", "stair climber", "jump rope"]
        result["workout_type"] = "cardio" if exercise in cardio_exercises else "strength"
        
        # Extract SETS (various patterns)
        sets_patterns = [
            r'(\d+)\s*(?:sets?|x)',
            r'(\d+)\s*set',
            r'did\s*(\d+)\s*set',
        ]
        for pattern in sets_patterns:
            match = re.search(pattern, text_lower)
            if match:
                result["sets"] = int(match.group(1))
                break
        
        # Extract REPS (various patterns)
        reps_patterns = [
            r'(?:x|×)\s*(\d+)\s*(?:reps?)?',
            r'(\d+)\s*(?:reps?|repetitions?)',
            r'sets?\s*(?:of\s*)?(\d+)',
            r'for\s*(\d+)\s*(?:reps?)?',
        ]
        for pattern in reps_patterns:
            match = re.search(pattern, text_lower)
            if match:
                result["reps"] = int(match.group(1))
                break
        
        # Extract WEIGHT (kg or lbs)
        weight_patterns = [
            r'(?:with|at|@)?\s*(\d+(?:\.\d+)?)\s*(?:kg|kgs?|kilos?)',
            r'(\d+(?:\.\d+)?)\s*kg',
            r'(\d+(?:\.\d+)?)\s*lbs?',
        ]
        for pattern in weight_patterns:
            match = re.search(pattern, text_lower)
            if match:
                weight = float(match.group(1))
                # Convert lbs to kg if needed
                if 'lb' in text_lower:
                    weight = weight * 0.453592
                result["weight_kg"] = weight
                break
        
        # Extract DURATION for cardio (hours and minutes)
        hour_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)', text_lower)
        min_match = re.search(r'(\d+)\s*(?:minutes?|mins?|min)', text_lower)
        
        if hour_match:
            result["duration_minutes"] = int(float(hour_match.group(1)) * 60)
        elif min_match:
            result["duration_minutes"] = int(min_match.group(1))
        
        # Extract DISTANCE
        km_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:km|kilometers?|k)', text_lower)
        mile_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:miles?|mi)', text_lower)
        
        if km_match:
            result["distance_km"] = float(km_match.group(1))
        elif mile_match:
            result["distance_km"] = float(mile_match.group(1)) * 1.60934
        
        return result if result else None
    
    def test_parsing(self):
        """Test the parser with various inputs"""
        test_cases = [
            "I did chest press of 25 kg 3 sets of 20 reps",
            "bench press 4x8 at 80kg",
            "ran for 30 minutes",
            "5km run in 25 minutes",
            "squats 5 sets 10 reps with 100kg",
            "3 sets of 12 bicep curls",
            "deadlift 5x5 @ 140kg",
            "swimming for 1 hour",
            "lat pulldown 3 sets 15 reps",
        ]
        
        print("🧪 Testing NLP Parser:\n")
        for test in test_cases:
            result = self.parse_workout(test)
            print(f"Input: {test}")
            print(f"Result: {result}\n")

# Test when run directly
if __name__ == "__main__":
    nlp = SmartFitnessNLP()
    nlp.test_parsing()
