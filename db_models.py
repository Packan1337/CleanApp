from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False, nullable=False)
    last_name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    profile_name = db.Column(db.String(50), unique=False, nullable=False)
    profile_type = db.Column(db.String(50), unique=False, nullable=False)
    user = db.relationship("User", backref="profiles")

    def __init__(self, user_id, profile_name, profile_type):
        self.user_id = user_id
        self.profile_name = profile_name
        self.profile_type = profile_type


class Tasks(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(50), unique=False, nullable=False)
    task_desc = db.Column(db.String(100), unique=False, nullable=False)
    task_weight = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, task_title, task_desc, task_weight):
        self.task_title = task_title
        self.task_desc = task_desc
        self.task_weight = task_weight


class Assigned_Tasks(db.Model):
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"), primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), primary_key=True)

    def __init__(self, task_id, profile_id):
        self.task_id = task_id
        self.profile_id = profile_id
