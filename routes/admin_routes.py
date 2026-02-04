from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_file
)
from models import db, Application, Admin
import openpyxl
from io import BytesIO

admin_bp = Blueprint("admin", __name__)

# -------------------------
# Admin Login
# -------------------------
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        admin = Admin.query.filter_by(
            username=username,
            password=password
        ).first()

        if admin:
            session["admin"] = True
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("admin/login.html")


# -------------------------
# Admin Dashboard
# -------------------------
@admin_bp.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    applications = Application.query.all()

    total = len(applications)
    pending = len([a for a in applications if a.status == "Pending"])
    approved = len([a for a in applications if a.status == "Approved"])
    rejected = len([a for a in applications if a.status == "Rejected"])

    return render_template(
        "admin/dashboard.html",
        applications=applications,
        total=total,
        pending=pending,
        approved=approved,
        rejected=rejected
    )


# -------------------------
# Approve Application
# -------------------------
@admin_bp.route("/approve/<int:id>")
def approve(id):
    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    application = Application.query.get_or_404(id)
    application.status = "Approved"
    db.session.commit()

    flash("Application approved successfully", "success")
    return redirect(url_for("admin.dashboard"))


# -------------------------
# Reject Application
# -------------------------
@admin_bp.route("/reject/<int:id>")
def reject(id):
    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    application = Application.query.get_or_404(id)
    application.status = "Rejected"
    db.session.commit()

    flash("Application rejected", "warning")
    return redirect(url_for("admin.dashboard"))


# -------------------------
# Download Excel
# -------------------------
@admin_bp.route("/download")
def download_excel():
    if not session.get("admin"):
        return redirect(url_for("admin.login"))

    applications = Application.query.all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Applications"

    # Header
    ws.append([
        "Application ID",
        "Name",
        "Email",
        "Phone",
        "Course",
        "Marks",
        "Status",
        "Applied On"
    ])

    # Data
    for app in applications:
        ws.append([
            app.application_id,
            app.name,
            app.email,
            app.phone,
            app.course,
            app.marks,
            app.status,
            app.created_at.strftime("%Y-%m-%d %H:%M")
        ])

    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)

    return send_file(
        stream,
        as_attachment=True,
        download_name="student_applications.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# -------------------------
# Logout
# -------------------------
@admin_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))
