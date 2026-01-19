from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    current_app,
)
from repositories.user_repo import get_user_by_username, verify_password

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    cfg = current_app.config

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            return render_template(
                "auth/login.html",
                error="Please enter both username and password",
            )

        user = get_user_by_username(cfg, username)
        if user and verify_password(password, user["password_hash"]):
            # Session setup
            session.clear()
            session["user_id"] = user["user_id"]
            session["role"] = user["role"]

            return redirect(_home_for_role(user["role"]))

        return render_template("auth/login.html", error="Invalid username/password")

    return render_template("auth/login.html")


@auth_bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def _home_for_role(role: str) -> str:
    """
    Route users to their role-specific home page.
    """
    if role == "patient":
        return url_for("patient.dashboard")
    if role == "clinician":
        return url_for("clinician.dashboard")
    # technician/admin -> admin pages
    return url_for("admin.users")
