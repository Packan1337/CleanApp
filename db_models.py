from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False, nullable=False)
    last_name = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)


class Profiles(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id", ondelete="CASCADE"))
    profile_name = db.Column(db.String(50), unique=False, nullable=False)
    profile_type = db.Column(db.String(50), unique=False, nullable=False)
    user = db.relationship("User", backref="profiles")
    assigned_tasks = db.relationship("AssignedTasks", backref="profile")


class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(50), unique=True, nullable=False)
    task_desc = db.Column(db.String(100), unique=False, nullable=False)
    task_weight = db.Column(db.Integer, unique=False, nullable=False)
    assignments = db.relationship("AssignedTasks", backref="task")

    def initialize_tasks():
        default_tasks = [
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
                "task_title": "Tvätta kläder2",
                "task_desc": "Fyll tvättmaskinen med nya kläder.",
                "task_weight": 5,
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

        new_task = cls(task_title=task_title,
                       task_desc=task_desc, task_weight=5)

        db.session.add(new_task)
        db.session.commit()

        return {"status": "success", "message": "Task added successfully!"}


class AssignedTasks(db.Model):
    __tablename__ = "assigned_tasks"
    task_id = db.Column(db.Integer, db.ForeignKey(
        "tasks.id", ondelete="CASCADE"), primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey(
        "profiles.id", ondelete="CASCADE"), primary_key=True)

    @classmethod
    def assign_task_to_profile(cls, task_id, profile_id):
        existing_assignment = cls.query.filter_by(
            task_id=task_id, profile_id=profile_id
        ).first()
        if existing_assignment:
            return {
                "status": "failure",
                "message": "The task is already assigned to this profile.",
            }

        assignment = cls(task_id=task_id, profile_id=profile_id)
        db.session.add(assignment)
        db.session.commit()

        return {
            "status": "success",
            "message": "Task successfully assigned to profile!",
        }
