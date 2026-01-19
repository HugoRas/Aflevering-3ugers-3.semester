import hashlib
from repositories.db import fetchone_dict, fetchall_dict, execute


def get_user_by_username(cfg, username: str):
    # NOTE: MariaDB connector uses ? placeholders (not %s)
    return fetchone_dict(cfg, "SELECT * FROM `user` WHERE username=?", (username,))


def verify_password(password: str, password_hash: str) -> bool:
    # Prototype hashing (SHA256). OK for prototype; bcrypt recommended in prod.
    return hashlib.sha256(password.encode("utf-8")).hexdigest() == password_hash


def create_user(cfg, username: str, password: str, role: str):
    pwd_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return execute(
        cfg,
        "INSERT INTO `user` (username, password_hash, role) VALUES (?,?,?)",
        (username, pwd_hash, role),
    )


def list_users(cfg):
    return fetchall_dict(cfg, "SELECT user_id, username, role FROM `user` ORDER BY user_id DESC")


def reset_password(cfg, user_id: int, new_password: str):
    pwd_hash = hashlib.sha256(new_password.encode("utf-8")).hexdigest()
    execute(cfg, "UPDATE `user` SET password_hash=? WHERE user_id=?", (pwd_hash, user_id))
