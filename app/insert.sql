INSERT INTO results VALUES (
    :created_datetime,
    :updated_datetime, 
    :scanned_datetime,
    :student_number,
    :test_id,
    :obtained_marks,
    :available_marks)
ON CONFLICT(student_number, test_id)
DO UPDATE SET 
    obtained_marks = MAX(obtained_marks, excluded.obtained_marks),
    available_marks = MAX(available_marks, excluded.available_marks),
    updated_datetime = excluded.updated_datetime