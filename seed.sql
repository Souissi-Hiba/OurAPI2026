-- Clears and seeds the admin user.
DELETE FROM users;
ALTER TABLE users AUTO_INCREMENT = 1;
INSERT INTO users (username, password)
VALUES ('admin', 'admin123');

-- Clears existing seed data and resets IDs.
DELETE FROM reports;
DELETE FROM students;
ALTER TABLE students AUTO_INCREMENT = 1;
ALTER TABLE reports AUTO_INCREMENT = 1;

-- Inserts one student.
INSERT INTO students (first_name, last_name, level, double_major)
VALUES ('Amine', 'Ben Salah', '3', 0);

-- Inserts one report.
INSERT INTO reports (
    title, type, keyword_1, keyword_2, keyword_3, release_date, student_id
)
VALUES (
    'Building a REST API with Flask',
    'internship',
    'flask',
    'api',
    'python',
    '2026-10-18',
    1
);
