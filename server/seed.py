from server.models import db, Exercise, Workout, WorkoutExercise
from server.app import app
from datetime import date

with app.app_context():

    print("Clearing old data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Seeding exercises...")
    squat = Exercise(name="Squat", category="Strength", equipment_needed=True)
    bench = Exercise(name="Bench Press", category="Strength", equipment_needed=True)
    plank = Exercise(name="Plank", category="Core", equipment_needed=False)
    jumping_jacks = Exercise(name="Jumping Jacks", category="Cardio", equipment_needed=False)

    exercises = [squat, bench, plank, jumping_jacks]
    db.session.add_all(exercises)
    db.session.commit()

    print("Seeding workouts...")
    workout1 = Workout(date=date(2025, 1, 20), duration_minutes=45, notes="Leg day — feeling strong!")
    workout2 = Workout(date=date(2025, 1, 21), duration_minutes=30, notes="Upper body focus")
    workout3 = Workout(date=date(2025, 1, 22), duration_minutes=20, notes="Quick core blast")

    workouts = [workout1, workout2, workout3]
    db.session.add_all(workouts)
    db.session.commit()

    print("Linking exercises to workouts...")
    we1 = WorkoutExercise(workout=workout1, exercise=squat, reps=10, sets=4)
    we2 = WorkoutExercise(workout=workout2, exercise=bench, reps=8, sets=3)
    we3 = WorkoutExercise(workout=workout3, exercise=plank, duration_seconds=60)
    we4 = WorkoutExercise(workout=workout3, exercise=jumping_jacks, duration_seconds=45)

    join_entries = [we1, we2, we3, we4]
    db.session.add_all(join_entries)
    db.session.commit()

    print("Database seeded successfully!")
