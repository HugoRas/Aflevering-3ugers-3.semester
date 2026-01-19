import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_USER = os.getenv("DB_USER", "st24")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "st24_DB_password")
    DB_NAME = os.getenv("DB_NAME", "st24_DB")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_ROOT = os.getenv("DATA_ROOT", os.path.join(BASE_DIR, "data"))

    RAW_DIR = os.path.join(DATA_ROOT, "uploads", "raw")
    FILTERED_DIR = os.path.join(DATA_ROOT, "uploads", "filtered")
    PLOTS_DIR = os.path.join(DATA_ROOT, "plots")

    LOG_DIR = os.getenv("LOG_DIR", os.path.join(BASE_DIR, "logs"))
