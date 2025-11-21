from flask import Flask
from flask_migrate import Migrate
from server.models import db  

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

if __name__ == '__main__':
    app.run(port=5555, debug=True)
