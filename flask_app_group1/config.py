import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    DB_HOST = os.getenv("DB_HOST", "DUMMY_HOST")
    DB_USER = os.getenv("DB_USER", "DUMMY_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "DUMMY_PASSWORD")
    DB_NAME = os.getenv("DB_NAME", "DUMMY_DB_NAME")
    DB_PORT = int(os.getenv("DB_PORT", "DUMMY_PORT"))

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_ROOT = os.getenv("DATA_ROOT", os.path.join(BASE_DIR, "data"))

    RAW_DIR = os.path.join(DATA_ROOT, "uploads", "raw")
    FILTERED_DIR = os.path.join(DATA_ROOT, "uploads", "filtered")
    PLOTS_DIR = os.path.join(DATA_ROOT, "plots")

    LOG_DIR = os.getenv("LOG_DIR", os.path.join(BASE_DIR, "logs"))
