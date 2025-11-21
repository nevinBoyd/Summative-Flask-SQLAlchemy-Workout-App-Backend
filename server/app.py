from flask import Flask, request, jsonify
from flask_migrate import Migrate
from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import exercise_schema, exercises_schema, workout_schema, workouts_schema  

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
    workout = Workout(
        date=data.get("date"),
        duration_minutes=data.get("duration_minutes"),
        notes=data.get("notes"),
    )
    db.session.add(workout)
    db.session.commit()
    return workout_schema.dump(workout), 201

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
    exercise = Exercise(
        name=data.get("name"),
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

if __name__ == '__main__':
    app.run(port=5555, debug=True)
