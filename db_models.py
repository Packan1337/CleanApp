from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(300))
    household_name = db.Column(db.String(15))
    profiles = db.relationship('Profiles', backref='user', lazy=True, cascade="all, delete-orphan")
    tasks = db.relationship('Tasks', backref='user', lazy=True, cascade="all, delete-orphan")
    


class Profiles(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profile_name = db.Column(db.String(50))
    profile_type = db.Column(db.String(50))
    assigned_tasks = db.relationship(
        'AssignedTasks', backref='profile', lazy=True, cascade="all, delete-orphan")


class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(100))
    task_desc = db.Column(db.String(200))
    task_weight = db.Column(db.Integer)
    task_type = db.Column(db.String(20))  # Can be 'default' or 'custom'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def initialize_tasks():
        default_tasks = [
            {
                "task_title": "Dammsuga",
                "task_desc": "Dammsug alla rum i hemmet.",
                "task_weight": 5,
                "task_type": "default",
            },
            {
                "task_title": "Moppa golvet",
                "task_desc": "Moppa golvet i hemmet.",
                "task_weight": 5,
                "task_type": "default",
            },
            {
                "task_title": "Diska",
                "task_desc": "Diska det som finns i handfatet.",
                "task_weight": 5,
                "task_type": "default",
            },
            {
                "task_title": "Fixa matlådor",
                "task_desc": "Laga mat och lägg in det i matlådor.",
                "task_weight": 5,
                "task_type": "default",
            },
            {
                "task_title": "Tvätta kläder",
                "task_desc": "Fyll tvättmaskinen med nya kläder.",
                "task_weight": 5,
                "task_type": "default",
            },
        ]

        tasks_dict = {task["task_title"]: task for task in default_tasks}

        existing_tasks = Tasks.query.all()
        existing_task_titles = set(task.task_title for task in existing_tasks)

        for task_title, task_data in tasks_dict.items():
            if task_title not in existing_task_titles:
                new_task = Tasks(
                    task_title=task_data["task_title"],
                    task_desc=task_data["task_desc"],
                    task_weight=task_data["task_weight"],
                    task_type=task_data["task_type"],
                    user_id=None,
                )
                db.session.add(new_task)

        db.session.commit()


class AssignedTasks(db.Model):
    __tablename__ = "assigned_tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey(
        'profiles.id'), nullable=False)
    task = db.relationship('Tasks', backref=db.backref(
        "assigned_task", uselist=False))
