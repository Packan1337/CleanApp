from flask import render_template, redirect, url_for, flash, request, Flask, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from db_models import db, User

app = Flask(__name__)
app.secret_key = 'secretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+mysqlconnector://kaliber:cleanapp@kaliber.mysql.pythonanywhere-services.com/kaliber$cleanapp_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        user = User.query.filter_by(email=request.form['email']).first()
        if user is None:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            hashed_password = generate_password_hash(password)
            new_user = User(first_name, last_name, email=email,
                            password=hashed_password)

            db.session.add(new_user)
            db.session.commit()

        else:
            flash(f"User: {user.email} already exists.", 'danger')
            return redirect(url_for('signup'))

        flash(f"User: {new_user.email} created successfully.", 'success')
        return redirect(url_for('login'))

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while adding the user: {str(e)}", 'danger')
        return redirect(url_for('signup'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['login-email']
        password = request.form['login-password']
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                session['user'] = user.email
                flash(
                    f"Successfully logged in as: {session['user']}.", 'success')
                return redirect(url_for('index'))
            else:
                flash('Incorrect password, try again.', 'danger')

        else:
            flash('Email does not exist.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Successfully logged out.', 'success')
    return redirect(url_for('login'))


# Run app #
# Remove this when deploying to pythonanywhere
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=80, debug=True)
