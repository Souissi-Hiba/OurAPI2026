# This is a Flask REST API for managing students and reports.
# It provides simple endpoints for a web services course project.
# The API keeps data in memory so the behavior is easy to understand.

import secrets
import time

from flask import Flask, jsonify, request

# ===== SETUP =====
app = Flask(__name__)

# ===== DATA =====
students = []
reports = []
next_student_id = 1
next_report_id = 1
current_token = None
token_expires_at = 0

# ===== HELPERS =====
def get_bearer_token():
    authorization = request.headers.get("Authorization")
    parts = authorization.split() if authorization else []
    if len(parts) == 2 and parts[0] == "Bearer":
        return parts[1]
    return ""


def check_token():
    authorization = request.headers.get("Authorization")
    if not authorization:
        return jsonify({"error": "Token required"}), 401

    token = get_bearer_token()

    if token != current_token:
        return jsonify({"error": "Invalid token"}), 403

    if time.time() > token_expires_at:
        return jsonify({"error": "Token expired"}), 401

    return None

# ===== HEALTH CHECK =====
@app.route("/")
def home():
    return "API is running"

# ===== REPORTS (public) =====
@app.route("/reports", methods=["POST"])
def create_report():
    global next_report_id

    data = request.get_json()
    report = {
        "id_r": next_report_id,
        "title": data["title"],
        "type": data["type"],
        "keyword_1": data["keyword_1"],
        "keyword_2": data["keyword_2"],
        "keyword_3": data["keyword_3"],
        "release_date": data["release_date"],
        "student_id": data["student_id"],
    }
    next_report_id += 1
    reports.append(report)

    return jsonify(report), 201


@app.route("/reports", methods=["GET"])
def get_all_reports():
    return jsonify(reports)


@app.route("/reports/<int:id_r>", methods=["GET"])
def get_report_by_id(id_r):
    for report in reports:
        if report["id_r"] == id_r:
            return jsonify(report)

    return jsonify({"error": "Report not found"}), 404


# ===== STUDENTS (private) =====
@app.route("/students", methods=["POST"])
def create_student():
    global next_student_id

    data = request.get_json()
    student = {
        "id_s": next_student_id,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "level": data["level"],
        "double_major": data["double_major"],
    }
    next_student_id += 1
    students.append(student)

    return jsonify(student), 201


@app.route("/students", methods=["GET"])
def get_all_students():
    token_error = check_token()
    if token_error:
        return token_error

    return jsonify(students)


@app.route("/students/<int:id_s>", methods=["GET"])
def get_student_by_id(id_s):
    token_error = check_token()
    if token_error:
        return token_error

    for student in students:
        if student["id_s"] == id_s:
            return jsonify(student)

    return jsonify({"error": "Student not found"}), 404


# ===== TOKEN =====
DEMO_USERNAME = "admin"
DEMO_PASSWORD = "admin123"
TOKEN_LIFETIME_SECONDS = 300


@app.route("/login", methods=["POST"])
def login():
    global current_token, token_expires_at

    data = request.get_json()

    if data.get("username") == DEMO_USERNAME and data.get("password") == DEMO_PASSWORD:
        token = secrets.token_hex()
        current_token = token
        token_expires_at = time.time() + TOKEN_LIFETIME_SECONDS
        return jsonify({
            "token": token,
            "expires_in": TOKEN_LIFETIME_SECONDS,
        }), 200

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/refresh", methods=["POST"])
def refresh():
    global current_token, token_expires_at

    if not request.headers.get("Authorization"):
        return jsonify({"error": "Token required"}), 401

    token = get_bearer_token()
    if token != current_token:
        return jsonify({"error": "Invalid token"}), 403

    current_token = secrets.token_hex()
    token_expires_at = time.time() + TOKEN_LIFETIME_SECONDS
    return jsonify({
        "token": current_token,
        "expires_in": TOKEN_LIFETIME_SECONDS,
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
    