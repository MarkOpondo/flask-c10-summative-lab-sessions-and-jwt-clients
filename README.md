# 🏋️ My Notes Application API

A modular Flask-based RESTful API designed to manage notes. The system utilizes JSON Web Tokens (JWT) for user security, Flask-SQLAlchemy for data interactions, and Marshmallow for data validation and parsing.

---

## 📂 Project Structure

```text
├── app
│   ├── __init__.py    # App factory configuration
│   ├── models.py      # SQLAlchemy models and Marshmallow schemas
│   └── routes.py      # RESTful routes and route handlers
├── app.py             # Main entry point file
├── config.py          # Environment settings profiles
├── instance
│   └── app.db         # Local SQLite database file
├── migrations         # Database tracking history folder
└── seed.py            # Development database data generation script
```

---

## 🚀 Installation & Setup

### 1. Initialize the Environment
Ensure Pipenv is installed globally, then configure your environment dependencies:
```bash
pipenv install
pipenv shell
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
JWT_SECRET_KEY=your_secure_random_key_string
FLASK_APP=app.py
FLASK_ENV=development
```

### 3. Run Database Migrations
Since migrations files already exist, push the schema directly to your local instance database file:
```bash
flask db upgrade
```

### 4. Seed Mock Data
Populate dummy database rows for testing:
```bash
python seed.py
```

---

## 🏃 Run Instructions

Launch the server locally with one of the following commands:

### Direct Python Execution
```bash
python app.py
```
The server will run on `http://127.0.0`.

---

## 🔑 API Endpoints Reference

| Method | Endpoint | Auth | Description |
| :--- | :--- | :---: | :--- |
| **GET** | `/` | ❌ | Returns the base workout app welcome payload. |
| **GET** | `/api/users` | ❌ | Fetches all users and their respective nested notes. |
| **POST** | `/api/signup` | ❌ | Registers a new user. Returns a signed access JWT. |
| **POST** | `/api/login` | ❌ | Validates credentials. Returns an access JWT token. |
| **GET** | `/api/notes` | 🔒 **JWT** | Fetches the caller's notes. Supports `?page=1&per_page=10`. |
| **POST** | `/api/notes` | 🔒 **JWT** | Creates a new note assigned to the calling user token. |
| **DELETE**| `/api/notes/<id>`| 🔒 **JWT** | Deletes a note by numeric ID if owned by the caller. |