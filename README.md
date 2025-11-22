# Workout Tracking API — Flask + SQLAlchemy Backend

A simple but capable backend API for tracking workouts, exercises, and performance details  
(reps, sets, or timed duration). Supports full CRUD operations across related fitness data.

Built using Flask, SQLAlchemy ORM, Marshmallow serialization, and SQLite.

---

## Features

- Track **Workouts** with date, duration, and notes
- Track **Exercises** with category + equipment requirement
- Associate exercises with workouts and log **reps / sets / duration**
- Full **CRUD** for all 3 resources
- JSON responses using Marshmallow schemas
- Cascading deletes keep relationships clean

---

## Tech Stack

| Component | Library |
|----------|---------|
| Framework | Flask |
| ORM | SQLAlchemy |
| Serialization | Marshmallow |
| Migrations | Flask-Migrate |
| Database | SQLite |

Python Version: **3.8.13+** ✔

---

## Installation

Clone the repository:

```bash
git clone https://github.com/nevinBoyd/Summative-Flask-SQLAlchemy-Workout-App-Backend.git
cd Summative-Flask-SQLAlchemy-Workout-App-Backend
pipenv install
pipenv run flask db init
pipenv run flask db migrate -m "Initial migration"
pipenv run flask db upgrade
pipenv run python server/seed.py
pipenv run flask run
```

Runs on:
http://127.0.0.1:5000

API Endpoints

### Workouts
| Method | Endpoint         | Description          |
| ------ | ---------------- | -------------------- |
| GET    | `/workouts`      | Get all workouts     |
| GET    | `/workouts/<id>` | Get a single workout |
| POST   | `/workouts`      | Create a new workout |
| DELETE | `/workouts/<id>` | Delete a workout     |

Example Create Workout:
curl -X POST http://127.0.0.1:5000/workouts \
-H "Content-Type: application/json" \
-d '{"date": "2025-01-20", "duration_minutes": 45, "notes": "Leg day — feeling strong!"}'

### Exercises
| Method | Endpoint          | Description           |
| ------ | ----------------- | --------------------- |
| GET    | `/exercises`      | Get all exercises     |
| GET    | `/exercises/<id>` | Get a single exercise |
| POST   | `/exercises`      | Create an exercise    |
| DELETE | `/exercises/<id>` | Delete an exercise    |

curl -X POST http://127.0.0.1:5000/exercises \
-H "Content-Type: application/json" \
-d '{"name": "Deadlift", "category": "Strength", "equipment_needed": true}'

curl -X DELETE http://127.0.0.1:5000/workout_exercises/5

---

🧪 Testing (Optional)

You can verify data after seeding by hitting:

http://127.0.0.1:5000/workouts

http://127.0.0.1:5000/workout_exercises

All endpoints can be tested via POSTMAN / Insomnia / cURL.

## Developer Notes

- Relationships required thought — cascades ensure data stays clean
- Marshmallow schemas help prevent circular JSON issues
- Using WorkoutExercise as a join table allows flexibility:
  reps-based OR duration-based exercises 
- Validations prevent nonsense (like negative duration)

```
server/
  ├── app.py
  ├── models.py
  ├── schemas.py
  ├── seed.py
migrations/
Pipfile
README.md
```

---

### Reflections & Takeaways

- Managing model relationships clicked once I used the join table
- Marshmallow + nested serialization helped structure clean API responses
- Database migrations + seeding made development much smoother
- Debugging cURL requests taught me how to trace request→response properly
- Structuring commits and PRs helped me follow a real-world workflow
  
