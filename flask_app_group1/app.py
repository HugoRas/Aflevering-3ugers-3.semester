import os
from flask import Flask, render_template, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from infrastructure.storage import ensure_dirs
from infrastructure.logging_conf import setup_logging


def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static"),
        static_url_path="/static",
    )

    # Running behind Apache reverse proxy on DBL webhost
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_prefix=1)

    app.config.from_object(Config)

    ensure_dirs(app.config)
    setup_logging(app.config)

    # --- DB schema init / migrations (prototype) ---
    # Ensure comment table exists (run once at startup, NOT per request)
    from repositories.comment_repo import ensure_comment_table
    ensure_comment_table(app.config)

    # Blueprints
    from controllers.auth import auth_bp
    from controllers.patient import patient_bp
    from controllers.clinician import clinician_bp
    from controllers.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp, url_prefix="/patient")
    app.register_blueprint(clinician_bp, url_prefix="/clinician")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.get("/health")
    def health():
        # Useful to verify proxy + app is running (no templates, no DB)
        return {"status": "ok"}

    @app.get("/")
    def landing():
        return render_template("index.html")

    @app.get("/dashboard")
    def dashboard():
        # Avoid exposing a public dashboard; send users to login instead
        return redirect(url_for("auth.login"))

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "63044"))
    app = create_app()
    app.run(host="0.0.0.0", port=port, debug=False)
