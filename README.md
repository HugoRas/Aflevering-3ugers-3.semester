# ECG Web System — Installation & Setup Guide

This repository contains a prototype ECG web system developed as part of a semester assignment.  
The system enables patients to upload ECG recordings, processes signals asynchronously, and allows clinicians to view filtered signals, plots, and comments through a web interface.

The system is implemented using **Flask (Python)**, **MariaDB**, and a **background worker** for signal processing.  
This README is intended as a **setup and operation guide** and does not contain environment-specific deployment details.

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
- Performs signal processing (filtering and analysis)
- Generates plots and stores output paths and processing status

#### Database (MariaDB)
- Stores users, roles, patients, recordings, signals, and clinician comments
- Acts as a coordination point between the web application and the worker

---

## Authentication, Sessions, and RBAC

Authentication logic resides in `controllers/auth.py`.  
User credentials are validated against hashed passwords using the `verify_password()` function. Passwords are never stored in plaintext.

Upon successful login, the user identifier (`user_id`) and role (`role`) are stored in the Flask session.  
Only minimal identity-related information is stored, and sessions are explicitly cleared on logout.

Authorization is enforced using a custom `require_role()` decorator.  
This implements **Role-Based Access Control (RBAC)** and adheres to the **principle of least privilege**, following established guidance from NIST.

---

## Deployment Model (Generic)

The system is designed to run behind a standard **Apache2** web server configuration.

- Static content may be served directly by Apache
- Dynamic requests are forwarded to the Flask application using a **reverse proxy**
- The Flask application should be executed using a WSGI server in production scenarios

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
cd flask_app_group1
