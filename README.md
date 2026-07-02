# EduPulse - Student Management System

A professional, responsive **Student Management System** built with **Flask**, **SQLAlchemy (SQLite)**, and a custom **Glassmorphic Vanilla CSS/JS** frontend. This application demonstrates clean software engineering principles like separation of concerns, the Flask application factory pattern, and proper security constructs for RESTful systems.

---

## 🌟 Key Features
- **Full CRUD Support**: Add, View, Update, and Delete students.
- **Dual-Layer Search**: Real-time interactive client-side search + backend database query search.
- **Rich Dashboard Stats**: Dynamically calculated KPIs (Total Students, Average GPA, Honor Roll counts).
- **Secure Destruction flow**: Multi-step delete confirmations inside custom modal dialogs.
- **Robust Field Validation**: Server and browser check for GPAs (0.0 to 4.0), email matches, and unique IDs.

---

## 📂 Directory Layout & Architectural Decisions
To keep our application tidy, professional, and scalable, we organized the structure as follows:

```
student/
├── app.py                      # Application entrypoint to run the Flask webserver
├── config.py                   # Central configurations (Database paths, Secret session keys)
├── requirements.txt            # Python environment dependency manifest
├── verify_db.py                # Database and ORM validation runner script
├── backend/                    # Core Python application package
│   ├── __init__.py             # Flask Application Factory initialization (create_app)
│   ├── database.py             # Database connector instantiation (Flask-SQLAlchemy)
│   ├── models/                 # ORM Database Schema Definitions
│   │   ├── __init__.py         # Exposes schemas cleanly to external packages
│   │   └── student.py          # Student SQLAlchemy Schema definition
│   └── routes/                 # Endpoint logic division (Flask Blueprints)
│       ├── __init__.py         # Exposes routes cleanly
│       └── student_routes.py   # Student CRUD, validation, and search routing
└── frontend/                   # Custom UI assets directory
    ├── templates/              # HTML layout files
    │   ├── base.html           # Universal shell (navigation, navbar, notifications system)
    │   ├── index.html          # Registry dashboard grid & metrics counters
    │   ├── add.html            # Registration form
    │   └── edit.html           # locked-key student details update form
    └── static/                 # Static Assets
        ├── css/
        │   └── style.css       # Premium custom stylesheet (custom dark theme, glow focus effects)
        └── js/
            └── main.js         # JavaScript interactivity (real-time filtering, delete modal control)
```

### 🧠 Why did we structure the project this way?

1. **Application Factory (`backend/__init__.py`)**: 
   - Instead of instantiating our Flask app globally inside a single file (like `app.py`), we use the application factory pattern (`create_app()`). This ensures configuration classes can change dynamically (e.g. swap SQLite config for PostgreSQL in production), and prevents database objects from creating circular imports with models or route handlers.
2. **Flask Blueprints (`backend/routes/`)**:
   - Blueprints split your routing logic into isolated components. The student management logic is entirely grouped within `student_routes.py`. If you want to build a "Course Registrations" or "Teacher Records" feature in the future, you simply create new blueprints, preventing `app.py` from growing into a massive, unreadable file.
3. **Database separation (`backend/database.py` and `backend/models/`)**:
   - Isolating ORM models from the routes allows for database migrations and query execution scripts (like `verify_db.py`) to easily import schemas without initializing the entire HTTP request lifecycle.
4. **Custom `frontend/` Folder**:
   - Flask normally looks for `/templates` and `/static` in the root folder. We override this configuration inside `create_app` to point to a consolidated `/frontend` directory. This keeps the client-side code completely separate from the backend application logic.

---

## 🛠️ Step-by-Step Installation Guide

To run this application locally on your computer, follow these simple terminal commands.

### 1. Set Up a Virtual Environment (Recommended)
Creating a virtual environment ensures Python libraries do not conflict with other system libraries:

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Project Dependencies
Use `pip` to install Flask and SQLAlchemy listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Run Database Integrity Checks (Verification Test)
Run the verification test script we wrote to confirm that the SQLite database engine initializes, reads, writes, and deletes records cleanly:
```bash
python verify_db.py
```
*(You will see a series of `[SUCCESS]` reports showing the full ORM lifecycle tests passing!)*

### 4. Launch the Web Application
Start the Flask development server:
```bash
python app.py
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 🛡️ Implementation Details & Security Practices

- **Preventing accidental GET deletions**: Destructive actions (like delete) use the standard POST method. If a crawler or link pre-fetcher visits the web links, it won't trigger delete logic because it only queries GET requests.
- **Read-Only Keys**: During a student update, the primary Student ID form field is marked `readonly` to prevent key tampering, and any attempts to force-change it are ignored.
- **State persistence on fail**: If an email is already registered or a GPA is invalid, Flask returns the user to the form with their inputs preserved and flash error indicators showing where they made a mistake.
