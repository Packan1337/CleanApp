from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

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

    def add_list_to_tasksdb():
        db.session.query(Tasks).filter(Tasks.task_id >= 0).delete()
        db.session.execute(text("ALTER TABLE Tasks AUTO_INCREMENT = 1"))
        db.session.commit()

        tasks = [
            {
                "task_title": "Dammsuga",
                "task_desc": "Dammsug alla rum i hemmet.",
                "task_weight": 5,
            },
            {
                "task_title": "Moppa golvet",
                "task_desc": "Moppa golvet i hemmet.",
                "task_weight": 5,
            },
            {
                "task_title": "Diska",
                "task_desc": "Diska det som finns i handfatet.",
                "task_weight": 5,
            },
            {
                "task_title": "Fixa matlådor",
                "task_desc": "Laga mat och lägg in det i matlådor.",
                "task_weight": 5,
            },
            {
                "task_title": "Tvätta kläder",
                "task_desc": "Fyll tvättmaskinen med nya kläder.",
                "task_weight": 5,
            },
            {
                "task_title": "Putsa fönster",
                "task_desc": "Test test test",
                "task_weight": 5,
            },
        ]

        for task in tasks:
            new_task = Tasks(
                task_title=task["task_title"],
                task_desc=task["task_desc"],
                task_weight=task["task_weight"],
            )
            db.session.add(new_task)
        db.session.commit()

    @classmethod
    def add_new_task(cls, task_title, task_desc):
        if not task_title or not task_desc:
            return {
                "status": "failure",
                "message": "Both title and description are required.",
            }

        new_task = cls(task_title=task_title, task_desc=task_desc, task_weight=5)

        db.session.add(new_task)
        db.session.commit()

        return {"status": "success", "message": "Task added successfully!"}


class AssignedTasks(db.Model):
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"), primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"), primary_key=True)

    def __init__(self, task_id, profile_id):
        self.task_id = task_id
        self.profile_id = profile_id
