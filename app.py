# This is a Flask REST API for managing students and reports.
# It provides simple endpoints for a web services course project.
# The API keeps data in memory so the behavior is easy to understand.

import secrets
import time

from db import get_connection
from flask import Flask, jsonify, request

# ===== SETUP =====
app = Flask(__name__)

# ===== DATA =====
current_token = None
token_expires_at = 0

# ===== HELPERS =====
def missing_field(data, fields):
    for field in fields:
        if field not in data:
            return field
    return None


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
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON body required"}), 400

    field = missing_field(data, [
        "title", "type", "keyword_1", "keyword_2",
        "keyword_3", "release_date", "student_id",
    ])
    if field:
        return jsonify({"error": f"Missing field: {field}"}), 400

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO reports (
            title, type, keyword_1, keyword_2, keyword_3,
            release_date, student_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            data["title"],
            data["type"],
            data["keyword_1"],
            data["keyword_2"],
            data["keyword_3"],
            data["release_date"],
            data["student_id"],
        ),
    )
    connection.commit()
    report_id = cursor.lastrowid
    connection.close()

    report = {
        "id_r": report_id,
        "title": data["title"],
        "type": data["type"],
        "keyword_1": data["keyword_1"],
        "keyword_2": data["keyword_2"],
        "keyword_3": data["keyword_3"],
        "release_date": data["release_date"],
        "student_id": data["student_id"],
    }

    return jsonify(report), 201


@app.route("/reports", methods=["GET"])
def get_all_reports():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reports")
    rows = cursor.fetchall()
    connection.close()

    return jsonify(rows)


@app.route("/reports/<int:id_r>", methods=["GET"])
def get_report_by_id(id_r):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reports WHERE id_r = %s", (id_r,))
    row = cursor.fetchone()
    connection.close()

    if row:
        return jsonify(row)

    return jsonify({"error": "Report not found"}), 404


@app.route("/reports/<int:id_r>", methods=["PUT"])
def update_report(id_r):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reports WHERE id_r = %s", (id_r,))
    row = cursor.fetchone()
    if not row:
        connection.close()
        return jsonify({"error": "Report not found"}), 404

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        connection.close()
        return jsonify({"error": "JSON body required"}), 400

    field = missing_field(data, [
        "title", "type", "keyword_1", "keyword_2",
        "keyword_3", "release_date", "student_id",
    ])
    if field:
        connection.close()
        return jsonify({"error": f"Missing field: {field}"}), 400

    cursor.execute(
        """
        UPDATE reports
        SET title = %s, type = %s, keyword_1 = %s, keyword_2 = %s,
            keyword_3 = %s, release_date = %s, student_id = %s
        WHERE id_r = %s
        """,
        (
            data["title"],
            data["type"],
            data["keyword_1"],
            data["keyword_2"],
            data["keyword_3"],
            data["release_date"],
            data["student_id"],
            id_r,
        ),
    )
    connection.commit()
    connection.close()

    report = {
        "id_r": id_r,
        "title": data["title"],
        "type": data["type"],
        "keyword_1": data["keyword_1"],
        "keyword_2": data["keyword_2"],
        "keyword_3": data["keyword_3"],
        "release_date": data["release_date"],
        "student_id": data["student_id"],
    }
    return jsonify(report), 200


@app.route("/reports/<int:id_r>", methods=["DELETE"])
def delete_report(id_r):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reports WHERE id_r = %s", (id_r,))
    row = cursor.fetchone()
    if not row:
        connection.close()
        return jsonify({"error": "Report not found"}), 404

    cursor.execute("DELETE FROM reports WHERE id_r = %s", (id_r,))
    connection.commit()
    connection.close()

    return jsonify({"message": "Report deleted"}), 200


# ===== STUDENTS (private) =====
@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON body required"}), 400

    field = missing_field(data, [
        "first_name", "last_name", "level", "double_major",
    ])
    if field:
        return jsonify({"error": f"Missing field: {field}"}), 400

    if data["double_major"] not in (0, 1):
        return jsonify({"error": "double_major must be 0 or 1"}), 400

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO students (first_name, last_name, level, double_major)
        VALUES (%s, %s, %s, %s)
        """,
        (
            data["first_name"],
            data["last_name"],
            data["level"],
            data["double_major"],
        ),
    )
    connection.commit()
    student_id = cursor.lastrowid
    connection.close()

    student = {
        "id_s": student_id,
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "level": data["level"],
        "double_major": data["double_major"],
    }

    return jsonify(student), 201


@app.route("/students", methods=["GET"])
def get_all_students():
    token_error = check_token()
    if token_error:
        return token_error

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    connection.close()

    return jsonify(rows)


@app.route("/students/<int:id_s>", methods=["GET"])
def get_student_by_id(id_s):
    token_error = check_token()
    if token_error:
        return token_error

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students WHERE id_s = %s", (id_s,))
    row = cursor.fetchone()
    connection.close()

    if row:
        return jsonify(row)

    return jsonify({"error": "Student not found"}), 404


# ===== TOKEN =====
TOKEN_LIFETIME_SECONDS = 300


@app.route("/login", methods=["POST"])
def login():
    global current_token, token_expires_at

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "JSON body required"}), 400

    field = missing_field(data, ["username", "password"])
    if field:
        return jsonify({"error": f"Missing field: {field}"}), 400

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = %s AND password = %s",
        (data["username"], data["password"]),
    )
    row = cursor.fetchone()
    connection.close()

    if row:
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


# ===== RUN =====
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
