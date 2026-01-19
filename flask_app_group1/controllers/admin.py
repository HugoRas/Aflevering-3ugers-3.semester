import os
from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    abort,
    send_from_directory,
    redirect,
    url_for,
)
from services.auth_service import require_role
from repositories.user_repo import list_users, create_user, reset_password
from repositories.patient_repo import ensure_patient_for_user

admin_bp = Blueprint("admin", __name__)

ALLOWED_ROLES = {"patient", "clinician", "admin", "technician"}


# -----------------------
# User list
# -----------------------
@admin_bp.get("/users")
@require_role("admin", "technician")
def users():
    cfg = current_app.config
    users_list = list_users(cfg)
    return render_template("admin/users.html", users=users_list)


# -----------------------
# Create user
# -----------------------
@admin_bp.post("/users/create")
@require_role("admin", "technician")
def users_create():
    cfg = current_app.config

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    role = (request.form.get("role") or "patient").strip()

    # (Optional) navn til patient-profil hvis felt findes i admin-form
    patient_name = (request.form.get("name") or "").strip() or None

    if not username or not password:
        abort(400, "Missing username or password")

    if role not in ALLOWED_ROLES:
        abort(400, "Invalid role")

    # Opret user
    user_id = create_user(cfg, username, password, role)

    # ✅ Auto-opret patient-profil hvis rollen er patient
    if role == "patient":
        ensure_patient_for_user(cfg, user_id, name=patient_name)

    return redirect(url_for("admin.users"))


# -----------------------
# Reset password
# -----------------------
@admin_bp.post("/users/<int:user_id>/reset")
@require_role("admin", "technician")
def users_reset(user_id):
    cfg = current_app.config
    new_password = request.form.get("new_password") or ""

    if not new_password:
        abort(400, "Missing new password")

    reset_password(cfg, user_id, new_password)
    return redirect(url_for("admin.users"))


# -----------------------
# Logs overview
# -----------------------
@admin_bp.get("/logs")
@require_role("admin", "technician")
def logs():
    return render_template("admin/logs.html")


# -----------------------
# Serve log file
# -----------------------
@admin_bp.get("/logs/file/<path:filename>")
@require_role("admin", "technician")
def logs_file(filename):
    """
    Serve log files to admin/technician.
    Basic security: prevent traversal and only allow common log-like extensions.
    """
    if ".." in filename or filename.startswith(("/", "\\")):
        abort(400)

    if not (filename.lower().endswith(".log") or filename.lower().endswith(".txt")):
        abort(404)

    log_dir = current_app.config["LOG_DIR"]
    full_path = os.path.join(log_dir, filename)
    if not os.path.isfile(full_path):
        abort(404)

    return send_from_directory(log_dir, filename)


# -----------------------
# DB page (placeholder)
# -----------------------
@admin_bp.get("/db")
@require_role("admin", "technician")
def db_page():
    return render_template("admin/db.html")
