# ECG Web System — Installation & Setup Guide

This repository contains a prototype ECG web system developed as part of a semester assignment.
The system enables patients to upload ECG recordings, processes signals asynchronously, and allows clinicians to view filtered signals, plots, and comments through a web interface.

The system is implemented using **Flask (Python)**, **MariaDB**, and a **background worker** for signal processing.  
This README is intended as a **setup and installation guide** and does not contain environment-specific deployment details.

---

## System Architecture Overview

The system follows a layered architecture inspired by the **Model–View–Controller (MVC)** pattern, separating presentation, application logic, and data access concerns.

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
- Acts as coordination point between the web application and the worker

---

## Authentication, Sessions, and RBAC

Authentication logic resides in `controllers/auth.py`.  
User credentials are validated against hashed passwords using `verify_password()`. Passwords are never stored in plaintext.

Upon successful login, the user identifier (`user_id`) and role (`role`) are stored in the Flask session.  
Only minimal identity-related information is stored, and sessions are cleared on logout.

Authorization is enforced using a custom `require_role()` decorator.  
This implements **Role-Based Access Control (RBAC)** and adheres to the **principle of least privilege**, following established guidance from NIST.

---

## Deployment Model (Generic)

The system is designed to run behind a standard **Apache2** web server configuration.

- Static content can be served directly by Apache.
- Dynamic requests are forwarded to the Flask application using a **reverse proxy**.
- The Flask application should be executed using a production WSGI server (e.g. Gunicorn).

This deployment model is commonly supported on university and shared Linux hosting environments.

---

## Requirements

- Linux-based operating system
- Python 3.10 or newer
- Git
- MariaDB Server
- Apache2
- `python3-venv`

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

---

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. Database setup (MariaDB)

Create a database and user:

```sql
CREATE DATABASE ecg_db;
CREATE USER 'ecg_user'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON ecg_db.* TO 'ecg_user'@'localhost';
FLUSH PRIVILEGES;
```

Update database credentials in the application configuration.

---

### 4. Filesystem setup

Create required runtime directories:

```bash
mkdir -p data/raw data/filtered data/plots logs
```

Ensure the application has write access to these directories.

---

## Running the System

### Development mode

```bash
flask.py run #PORTNUMBER
python processor.py
```

- The Flask application handles HTTP requests
- The background worker processes queued ECG recordings

---

## Production Considerations

- Run the Flask application behind Apache using a reverse proxy
- Use a WSGI server
- Enable HTTPS in production environments
- Restrict filesystem and database permissions according to least privilege

---

## Verification Checklist

- Application reachable through web server
- Authentication and RBAC function correctly
- ECG upload succeeds
- Background processing completes
- Plots and results are accessible to authorized users

---

## Notes

- This system is a **prototype**
- Password hashing uses SHA-256
- The background worker must be running for signal processing to occur
