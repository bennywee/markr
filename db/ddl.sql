CREATE TABLE IF NOT EXISTS results (
    created_datetime TEXT NOT NULL,
    updated_datetime TEXT NOT NULL,
    scanned_datetime TEXT NOT NULL,
    student_number TEXT NOT NULL, 
    test_id TEXT NOT NULL,
    obtained_marks INT,
    available_marks INT,
    PRIMARY KEY (student_number, test_id)
)