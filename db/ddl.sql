CREATE TABLE IF NOT EXISTS results (
    created_datetime TEXT NOT NULL,
    updated_datetime TEXT NOT NULL,
    scanned_datetime TEXT NOT NULL,
    student_number TEXT NOT NULL, 
    test_id TEXT NOT NULL,
    obtained_marks INT CHECK(typeof(obtained_marks) = 'integer'),
    available_marks INT CHECK(typeof(available_marks) = 'integer'),
    PRIMARY KEY (student_number, test_id)
)
