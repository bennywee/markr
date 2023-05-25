SELECT ROUND(CAST(obtained_marks AS REAL) / CAST(available_marks AS REAL) * 100,1) AS perc
FROM results 
WHERE test_id = :test_id