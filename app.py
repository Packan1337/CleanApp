from flask import render_template, redirect, url_for, flash, request, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from db_models import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://kaliber:cleanapp@kaliber.mysql.pythonanywhere-services.com/kaliber$cleanapp_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def insert_user():
    new_user = User(
        first_name='testuser',
        last_name="testname",
        password="asd",
        email='testuser@example.com')

    db.session.add(new_user)
    db.session.commit()


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
# Remove this when deploying to pythonanywhere
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=80, debug=True)
