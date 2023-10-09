from flask import render_template, redirect, url_for, flash, request, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from db_models import db, User
import MySQLdb

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://kaliber:cleanapp@kaliber.mysql.pythonanywhere-services.com/kaliber$cleanapp_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

# Run app #
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)