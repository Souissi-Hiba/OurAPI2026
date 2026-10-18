# This is a Flask REST API for managing students and reports.
# It provides simple endpoints for a web services course project.
# The API keeps data in memory so the behavior is easy to understand.

from flask import Flask, jsonify, request

# ===== SETUP =====
app = Flask(__name__)

# ===== DATA =====
students = []
reports = []
next_student_id = 1
next_report_id = 1

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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)