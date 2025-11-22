from marshmallow import Schema, fields, validate

# Serializing/deserializing execise model data
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()

# WorkoutExercise association table
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True, load_only=True)
    exercise_id = fields.Int(required=True, load_only=True)

    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()

    exercise = fields.Nested("ExerciseSchema", dump_only=True)

# Schema for workout model
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int()
    notes = fields.Str()

    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)

# Schema instances for use in API routes
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
