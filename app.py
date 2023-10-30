from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    Flask,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash
from db_models import db, User, Profiles, Tasks, AssignedTasks
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = "secretkey"

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://kaliber:cleanapp@kaliber.mysql.pythonanywhere-services.com/kaliber$cleanapp_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()
    Tasks.initialize_tasks()


@app.route("/index")
def index():
    today = date.today()
    current_week_number = today.isocalendar()[1]

    if "user" in session:
        user_email = session["user"]
        user = User.query.filter_by(email=user_email).first()

        if user:
            profiles = Profiles.query.filter_by(user_id=user.id).all()
        else:
            flash("User does not exist.", "danger")
            return redirect(url_for("login"))
    else:
        flash("Please log in to view this page.", "danger")
        return redirect(url_for("login"))

    return render_template("index.html", profiles=profiles, week_number=current_week_number, today=today)


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/add_user", methods=["POST"])
def add_user():
    try:
        user = User.query.filter_by(email=request.form["email"]).first()
        if user is None:
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["password"]
            hashed_password = generate_password_hash(password)

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password
            )

            db.session.add(new_user)
            db.session.commit()

        else:
            flash(f"User: {user.email} already exists.", "danger")
            return redirect(url_for("signup"))

        flash(f"User: {new_user.email} created successfully.", "success")
        return redirect(url_for("login"))

    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while adding the user: {str(e)}", "danger")
        return redirect(url_for("signup"))


@app.route("/reset_password_page")
def reset_password_page():
    return render_template("reset_password.html")


@app.route("/reset_password", methods=["POST"])
def reset_password():
    email = request.form.get("email")
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    new_password_repeat = request.form.get("new_password_repeat")

    if new_password != new_password_repeat:
        flash("Passwords do not match!", "danger")
        return redirect(url_for("reset_password_page"))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("User with the provided email does not exist!", "danger")
        return redirect(url_for("reset_password_page"))

    if not check_password_hash(user.password, current_password):
        flash("Current password is incorrect!", "danger")
        return redirect(url_for("reset_password_page"))

    user.password = generate_password_hash(new_password)

    db.session.commit()

    flash("Password successfully updated!", "success")
    return redirect(url_for("login"))

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["login-email"]
        password = request.form["login-password"]
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                session["user"] = user.email
                flash(
                    f"Successfully logged in as: {session['user']}.", "success")
                return redirect(url_for("index"))
            else:
                flash("Incorrect password, try again.", "danger")

        else:
            flash("Email does not exist.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Successfully logged out.", "success")
    return redirect(url_for("login"))


@app.route("/profile_manager")
def profile_manager():
    if "user" not in session:
        flash("Please log in to view this page.", "danger")
        return redirect(url_for("login"))
    else:
        user = User.query.filter_by(email=session["user"]).first()
        if user:
            profiles = user.profiles
        else:
            profiles = []
        return render_template("profile_manager.html", profiles=profiles)


@app.route("/add_profile", methods=["POST"])
def add_profile():
    try:
        user = User.query.filter_by(email=session["user"]).first()
        if user is None:
            flash(f"User: {user.email} does not exist.", "danger")
            return redirect(url_for("profile_manager"))

        else:
            user_id = user.id
            profile_name = request.form["profile_name"]
            profile_type = request.form["profile_type"]

            new_profile = Profiles(
                user_id=user_id,
                profile_name=profile_name,
                profile_type=profile_type
            )

            db.session.add(new_profile)
            db.session.commit()

            flash(
                f"Profile: {new_profile.profile_name} created successfully.", "success"
            )
            return redirect(url_for("profile_manager"))

    except Exception as e:
        db.session.rollback()
        flash(
            f"An error occurred while adding the profile: {str(e)}", "danger")
        return redirect(url_for("profile_manager"))


@app.route("/delete_profile/<int:profile_id>", methods=["POST"])
def delete_profile(profile_id):
    profile = Profiles.query.get_or_404(profile_id)
    try:
        db.session.delete(profile)
        db.session.commit()
        flash("Profile deleted successfully.", "success")
    except Exception as e:
        print(e)
        db.session.rollback()
        flash("Error deleting profile.", "danger")
    return redirect(url_for("profile_manager"))


@app.route("/edit_profile/<int:profile_id>", methods=["POST"])
def edit_profile(profile_id):
    profile = Profiles.query.get_or_404(profile_id)
    new_name = request.form.get("new_name")
    if new_name:
        profile.profile_name = new_name
        db.session.commit()
        flash("Profile name updated successfully.", "success")
    else:
        flash("Invalid name.", "danger")
    return redirect(url_for("profile_manager"))


@app.route("/task_management")
def task_management():
    if "user" in session:
        user_email = session["user"]
        user = User.query.filter_by(email=user_email).first()

        if user:
            profiles = user.profiles
        else:
            flash("User does not exist.", "danger")
            return redirect(url_for("login"))

    else:
        flash("Please log in to view this page.", "danger")
        return redirect(url_for("login"))

    tasks = Tasks.query.all()

    return render_template("task_management.html", profiles=profiles, tasks=tasks)


@app.route("/add_custom_task", methods=["POST"])
def add_custom_task():
    custom_task = request.form["custom-task-input"]
    custom_task_description = request.form["custom-task-description"]
    if custom_task:
        new_task = Tasks(task_title=custom_task,
                         task_desc=custom_task_description, task_weight=5)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully.", "success")
    else:
        flash("Invalid task name.", "danger")

    return redirect(url_for("task_management"))


@app.route("/assign_tasks", methods=["POST"])
def assign_tasks():
    task_id = request.form.get("task_id")
    profile_id = request.form.get("profile_id")

    try:
        task_id = int(task_id)
        profile_id = int(profile_id)
    except ValueError:
        flash("Invalid task or profile ID.", "danger")
        return redirect(url_for("task_management"))

    try:
        new_assigned_task = AssignedTasks(
            task_id=task_id,
            profile_id=profile_id,
        )

        db.session.add(new_assigned_task)
        db.session.commit()
        flash("Task assigned successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(
            f"An error occurred while assigning the task: {str(e)}", "danger")

    return redirect(url_for("task_management"))


# Run app #
# Remove this when deploying to pythonanywhere
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
