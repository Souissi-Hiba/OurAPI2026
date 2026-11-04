# Project rules
Student project: Flask REST API (Part 1 of web services course).

## Scope
- Part 2: data is stored in MySQL (database university, tables students and reports) instead of lists. MySQL runs in the Docker container part2-mysql on 127.0.0.1 port 3307, never port 3306. The token stays in two simple variables (current_token, token_expires_at). Use plain SQL queries with PyMySQL. No ORM, no SQLAlchemy.
- Only Flask and PyMySQL. Do not install other libraries unless I ask.
- Everything stays in app.py, except db.py for the database connection, schema.sql for the table definitions and seed.sql for the demo data. Do not create other files or folders unless I ask.
- Only build the endpoints listed in README.md.

## Style
- Beginner-friendly code: simple names, short comments, plain functions.
- No classes, blueprints, or advanced patterns.
- Errors return JSON like {"error": "message"} with the right status code.

## Code story (the teacher reads the code)
- app.py must read top to bottom like a story, in this order:
  setup -> data -> helpers -> public routes (reports) -> private routes (students) -> token -> errors -> run.
- Mark each part with a banner comment, e.g. # ===== REPORTS (public) =====
- Students and reports use the same pattern and mirrored names
  (create_report / create_student, get_all_reports / get_all_students).
- Comments explain WHY, not what. Keep them short.
- No dead code, no leftover or generic AI comments.

## Behavior
- Do only what the prompt asks, nothing extra. Do not refactor working code.
- Run git commands only when I ask. Add files by name, never `git add .`.
- Never add Co-authored-by or any Copilot/AI mention to a commit message. I am the only author.
- Never commit or push ROADMAP.md, STORY.md or PROMPTS.md (they are private).
- For anything bigger than one route, show a short plan first and wait for my OK.
- Windows + .venv. Run with: .venv\Scripts\python.exe app.py