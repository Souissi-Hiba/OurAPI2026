# This is a Flask REST API for managing students and reports.
# It provides simple endpoints for a web services course project.
# The API keeps data in memory so the behavior is easy to understand.

from flask import Flask

# ===== SETUP =====
app = Flask(__name__)

# ===== DATA =====
students = []
reports = []
next_student_id = 1
next_report_id = 1


@app.route("/")
def home():
    return "API is running"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)