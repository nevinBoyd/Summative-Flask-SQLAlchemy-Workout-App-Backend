from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

# Exercise model
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean, default=False)

    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', cascade="all, delete")
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises')
    
    # Field validation
    @validates('name')
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Exercise name must be provided.")
        
        return value

    @validates('category')
    def validate_category(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Exercise category must be provided.")
        
        return value

# Workout model
class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercise', backref='workout', cascade="all, delete")
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts')
    
    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is not None and value < 0:
            raise ValueError("Workout duration must be a positive number.")
        
        return value

# Join table ~ associated model
class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    
    # Optional performance details
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)
    
    # Prevent negative workout metrics validation
    @validates('reps', 'sets', 'duration_seconds')
    def validate_positive_int(self, key, value):
        if value is not None and value < 0:
            raise ValueError(f"{key} must be a positive integer.")
        
        return value
