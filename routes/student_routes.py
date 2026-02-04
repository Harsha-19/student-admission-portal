import uuid
from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Application

student_bp = Blueprint("student", __name__)

@student_bp.route("/")
def home():
    return render_template("home.html")

@student_bp.route("/apply", methods=["GET", "POST"])
def apply():
    if request.method == "POST":
        app_id = str(uuid.uuid4())[:8]

        application = Application(
            application_id=app_id,
            name=request.form["name"],
            email=request.form["email"],
            phone=request.form["phone"],
            course=request.form["course"],
            marks=request.form["marks"]
        )

        db.session.add(application)
        db.session.commit()

        return redirect(url_for("student.status", app_id=app_id))

    return render_template("apply.html")

@student_bp.route("/status")
def status():
    app_id = request.args.get("app_id")
    application = Application.query.filter_by(application_id=app_id).first()
    return render_template("status.html", application=application)
