from functools import wraps
from flask import session, redirect, url_for, abort

def require_role(*roles):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("auth.login"))

            role = session.get("role")
            if role not in roles:
                abort(403, description=f"Role '{role}' not permitted")

            return fn(*args, **kwargs)
        return wrapper
    return deco
