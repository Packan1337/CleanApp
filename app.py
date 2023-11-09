from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    Flask,
    session,
    jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from db_models import db, User, Profiles, AssignedTasks, Tasks
from datetime import date

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

#################### INDEX ####################


@app.route("/index")
def index():
    if "user" in session:
        user_email = session["user"]
        user = User.query.filter_by(email=user_email).first()

        if user:
            profiles = user.profiles
        else:
            flash("Användaren existerar inte.", "danger")
            return redirect(url_for("login"))

        # Get the current date and week number
        today = date.today().strftime('%Y-%m-%d')
        current_week_number = date.today().isocalendar()[1]

        return render_template("index.html", profiles=profiles, week_number=current_week_number, today=today)
    else:
        flash("Vänligen logga in för att se denna sida.", "danger")
        return redirect(url_for("login"))

#################### USER SIGNUP ####################


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
            flash(f"Användare: {user.email} finns redan.", "danger")
            return redirect(url_for("signup"))

        flash(f"Användare: {new_user.email} har skapats!", "success")
        return redirect(url_for("login"))

    except Exception as e:
        db.session.rollback()
        flash(
            f"Ett error uppstod vid försök att lägga till användaren: {str(e)}", "danger")
        return redirect(url_for("signup"))

#################### PASSWORD RESET ####################


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
        flash("Lösenorden matchar inte!", "danger")
        return redirect(url_for("reset_password_page"))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("En användare med den e-mailen existerar inte!", "danger")
        return redirect(url_for("reset_password_page"))

    if not check_password_hash(user.password, current_password):
        flash("Lösenordet är inte korrekt!", "danger")
        return redirect(url_for("reset_password_page"))

    user.password = generate_password_hash(new_password)

    db.session.commit()

    flash("Lösenordet har uppdaterats!", "success")
    return redirect(url_for("login"))

#################### LOGIN/LOGOUT ####################


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
                    f"Du har loggats in som: {session['user']}.", "success")
                return redirect(url_for("index"))
            else:
                flash("Fel lösenord, försök igen.", "danger")

        else:
            flash("Email:en existerar inte", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Du har loggats ut.", "success")
    return redirect(url_for("login"))

#################### PROFILE MANAGEMENT ####################


@app.route("/profile_manager")
def profile_manager():
    if "user" not in session:
        flash("Vänligen logga in för att se denna sida.", "danger")
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
            flash(f"Användare: {user.email} existerar inte.", "danger")
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
                f"Profilen: {new_profile.profile_name} har skapats.", "success"
            )
            return redirect(url_for("profile_manager"))

    except Exception as e:
        db.session.rollback()
        flash(
            f"Ett error uppstod vid försök att lägga till profilen: {str(e)}", "danger")
        return redirect(url_for("profile_manager"))

#################### PROFILE DELETE/EDIT ####################


@app.route("/delete_profile/<int:profile_id>", methods=["POST"])
def delete_profile(profile_id):
    profile = Profiles.query.get_or_404(profile_id)
    try:
        db.session.delete(profile)
        db.session.commit()
        flash("Profilen har raderats.", "success")
    except Exception as e:
        print(e)
        db.session.rollback()
        flash("Ett error uppstod vid försök att radera profilen.", "danger")
    return redirect(url_for("profile_manager"))


@app.route("/edit_profile/<int:profile_id>", methods=["POST"])
def edit_profile(profile_id):
    profile = Profiles.query.get_or_404(profile_id)
    new_name = request.form.get("new_name")
    if new_name:
        profile.profile_name = new_name
        db.session.commit()
        flash("Profil-namnet är uppdaterat!", "success")
    else:
        flash("Felaktigt namn.", "danger")
    return redirect(url_for("profile_manager"))

#################### TASK MANAGEMENT ####################


@app.route("/task_management")
def task_management():
    if "user" in session:
        user_email = session["user"]
        user = User.query.filter_by(email=user_email).first()

        if user:
            profiles = user.profiles
            custom_tasks = Tasks.query.filter_by(user_id=user.id).all()
            default_tasks = Tasks.query.filter_by(user_id=None).all()
            tasks = default_tasks + custom_tasks
        else:
            flash("Användaren existerar inte.", "danger")
            return redirect(url_for("login"))

    else:
        flash("Vänligen logga in för att se denna sida.", "danger")
        return redirect(url_for("login"))

    return render_template("task_management.html", profiles=profiles, tasks=tasks)


@app.route("/add_custom_task", methods=["POST"])
def add_custom_task():
    user = User.query.filter_by(email=session["user"]).first()
    custom_task_title = request.form["custom-task-input"]
    custom_task_description = request.form["custom-task-description"]

    if custom_task_title:
        new_task = Tasks(task_title=custom_task_title, task_desc=custom_task_description,
                         task_weight=5, task_type="custom", user_id=user.id)
        db.session.add(new_task)
        db.session.commit()
        flash(
            f"Uppgiften: '{new_task.task_title}' har lagts till!.", "success")
    else:
        flash("Felaktigt uppgifts-namn.", "danger")

    return redirect(url_for("task_management"))


@app.route("/assign_tasks", methods=["POST"])
def assign_tasks():
    task_ids = request.form.getlist("task_ids[]")
    profile_ids = request.form.getlist("profile_ids[]")

    try:
        task_ids = [int(task_id) for task_id in task_ids]
        profile_ids = [int(profile_id) for profile_id in profile_ids]
    except ValueError:
        flash("Felaktigt uppgifts eller profil id.", "danger")
        return redirect(url_for("task_management"))

    try:
        for task_id in task_ids:
            for profile_id in profile_ids:
                new_assigned_task = AssignedTasks(
                    task_id=task_id,
                    profile_id=profile_id,
                )
                db.session.add(new_assigned_task)
        db.session.commit()
        flash("Uppgifterna har tilldelats!", "success")
    except Exception as e:
        db.session.rollback()
        flash(
            f"Ett error uppstod vid försök att tilldela uppgifterna: {str(e)}", "danger")

    return redirect(url_for("task_management"))


#################### TASK DELETE/EDIT ####################

@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash("Uppgiften har raderats.", "success")
        return jsonify(status="success")
    except Exception as e:
        print(e)
        db.session.rollback()
        flash("Ett error uppstod vid försök att radera uppgiften.", "danger")
        return jsonify(status="error"), 500


# Task edit
@app.route("/edit_task/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    new_name = request.form.get("new_name")
    new_desc = request.form.get("new_desc")
    new_weight = request.form.get("new_weight")
    if new_name:
        task.task_title = new_name
        task.task_desc = new_desc
        task.task_weight = new_weight
        db.session.commit()
        flash("Uppgiften är uppdaterad!.", "success")
    else:
        flash("Felaktigt uppgifts-namn.", "danger")
    return redirect(url_for("task_management"))


# Run app #
# Remove this when deploying to pythonanywhere
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
