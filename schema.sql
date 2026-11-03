-- Stores students.
CREATE TABLE students (
    id_s INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    level VARCHAR(20) NOT NULL,
    double_major TINYINT(1) NOT NULL
);

-- Stores student reports.
CREATE TABLE reports (
    id_r INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    type VARCHAR(50) NOT NULL,
    keyword_1 VARCHAR(50) NOT NULL,
    keyword_2 VARCHAR(50) NOT NULL,
    keyword_3 VARCHAR(50) NOT NULL,
    release_date DATE NOT NULL,
    student_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id_s)
);
