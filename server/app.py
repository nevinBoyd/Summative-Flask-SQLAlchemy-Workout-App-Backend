from flask import Flask, request, jsonify
from flask_migrate import Migrate
from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import (
    exercise_schema, 
    exercises_schema, 
    workout_schema, 
    workouts_schema,
    WorkoutExerciseSchema
)      
from datetime import datetime

app = Flask(__name__)

# Database config (SQLite in project root)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Simple root route for sanity check
@app.route('/')
def index():
    
    return "Workout API is running!"

# GET all workouts
@app.get('/workouts')
def get_workouts():
    workouts = Workout.query.all()
    return workouts_schema.dump(workouts), 200

# GET single workout
@app.get('/workouts/<int:id>')
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return {"error": "Workout not found"}, 404
    return workout_schema.dump(workout), 200

# POST workout
@app.post('/workouts')
def create_workout():
    data = request.get_json()

    errors = workout_schema.validate(data)
    if errors:
        return {"errors": errors}, 400
    
    try:
        workout = Workout(
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            duration_minutes=data.get("duration_minutes"),
            notes=data.get("notes"),
        )

        db.session.add(workout)
        db.session.commit()
        return workout_schema.dump(workout), 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
    
# DELETE workout
@app.delete('/workouts/<int:id>')
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return {"error": "Workout not found"}, 404
    
    db.session.delete(workout)
    db.session.commit()
    return {"message": "Workout deleted"}, 200


# GET all exercises
@app.get('/exercises')
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises), 200

# GET single exercise
@app.get('/exercises/<int:id>')
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return {"error": "Exercise not found"}, 404
    return exercise_schema.dump(exercise), 200

# POST exercise
@app.post('/exercises')
def create_exercise():
    data = request.get_json()

    errors = exercise_schema.validate(data)
    if errors:
        return {"errors": errors}, 400
    
    exercise = Exercise(
        name=data["name"],
        category=data.get("category"),
        equipment_needed=data.get("equipment_needed", False),
    )
    db.session.add(exercise)
    db.session.commit()
    return exercise_schema.dump(exercise), 201

# DELETE exercise
@app.delete('/exercises/<int:id>')
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return {"error": "Exercise not found"}, 404
    
    db.session.delete(exercise)
    db.session.commit()
    return {"message": "Exercise deleted"}, 200

@app.post('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises')
def add_workout_exercise(workout_id, exercise_id):
    data = request.get_json()

    workout = Workout.query.get(workout_id)
    if not workout:
        return {"error": "Workout not found"}, 404
    
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return {"error": "Exercise not found"}, 404

    new_link = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=data.get("reps"),
        sets=data.get("sets"),
        duration_seconds=data.get("duration_seconds")
    )

    db.session.add(new_link)
    db.session.commit()

    return workout_schema.dump(workout), 201

# GET all workout_exercises
@app.get('/workout_exercises')
def get_all_workout_exercises():
    links = WorkoutExercise.query.all()
    return WorkoutExerciseSchema(many=True).dump(links), 200

# GET workout_exercise by id
@app.get('/workout_exercises/<int:id>')
def get_workout_exercise(id):
    link = WorkoutExercise.query.get(id)
    if not link:
        return {"error": "WorkoutExercise not found"}, 404
    return WorkoutExerciseSchema().dump(link), 200

# PATCH workout_exercise
@app.patch('/workout_exercises/<int:id>')
def update_workout_exercise(id):
    link = WorkoutExercise.query.get(id)
    if not link:
        return {"error": "WorkoutExercise not found"}, 404

    data = request.get_json()

    if "reps" in data:
        link.reps = data["reps"]
    if "sets" in data:
        link.sets = data["sets"]
    if "duration_seconds" in data:
        link.duration_seconds = data["duration_seconds"]

    db.session.commit()
    return WorkoutExerciseSchema().dump(link), 200

# DELETE workout_exercise
@app.delete('/workout_exercises/<int:id>')
def delete_workout_exercise(id):
    link = WorkoutExercise.query.get(id)
    if not link:
        return {"error": "WorkoutExercise not found"}, 404
    
    db.session.delete(link)
    db.session.commit()
    return {"message": "WorkoutExercise deleted"}, 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
