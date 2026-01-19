# ECG Web System — Installation & Technical Overview

This repository contains a prototype ECG web system developed as part of a 3-week semester assignment.  
The system enables patients to upload ECG recordings from home, processes the signals asynchronously, and allows clinicians to view filtered signals, plots, and comments through a web interface.

The system is implemented using **Flask (Python)**, **MariaDB**, and a **background worker** for signal processing, and is intended to run on a Linux-based server environment.

---

## System Architecture Overview

The system follows a layered architecture inspired by the **Model–View–Controller (MVC)** pattern and separates concerns across presentation, application logic, and data access layers.

### Main Components

#### Flask Web Application
- Handles HTTP requests and responses
- Implements authentication and **Role-Based Access Control (RBAC)**
- Provides web interfaces for patients, clinicians, and administrators
- Receives ECG uploads (`.dat` + `.hea`) and stores metadata in the database

#### Background Worker
- Runs independently of the web application
- Polls the database for queued ECG recordings
- Performs signal processing (filtering, feature extraction)
- Generates plots and stores output paths and processing status

#### Database (MariaDB)
- Stores users, roles, patients, recordings, signals, and clinician comments
- Acts as coordination point between web application and worker

---

## Authentication, Sessions, and RBAC

Authentication logic resides in `controllers/auth.py`.  
User credentials are validated against hashed passwords using `verify_password()`.  
Passwords are never stored in plaintext.

Upon successful login, the user identifier (`user_id`) and role (`role`) are stored in the Flask session.  
Only minimal identity-related information is stored, and sessions are cleared on logout.

Authorization is enforced using a custom `require_role()` decorator.  
This implements RBAC and adheres to the **principle of least privilege**.  
The RBAC model follows guidance from **NIST**.

---

## Requirements

- Linux (Ubuntu / Debian recommended)
- Python 3.10 or newer
- Git
- MariaDB Server
- Apache2
- `python3-venv`

---

## Installation

### 1. Clone repository

```bash
git clone https://github.com/HugoRas/Aflevering-3ugers-3.semester.git
cd Aflevering-3ugers-3.semester
```

### 2. Virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Database setup

```sql
CREATE DATABASE ecg_db;
CREATE USER 'ecg_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON ecg_db.* TO 'ecg_user'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Filesystem setup

```bash
mkdir -p data/raw data/filtered data/plots logs
```

---

## Running the System

### Development

```bash
flask run
python processor.py
```

---

## Production

Run the Flask application behind **Apache reverse proxy** and **Gunicorn**.

---

## Verification

- Login works
- Upload works
- Processing completes
- Plots are visible
- RBAC is enforced

---

## Notes

- Prototype system
- Password hashing uses SHA-256
- Background worker must be running
