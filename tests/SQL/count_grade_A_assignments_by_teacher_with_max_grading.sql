-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH GradingCounts AS (
    SELECT
        teacher_id,
        COUNT(*) AS grading_count
    FROM
        assignments
    WHERE
        grade IS NOT NULL
    GROUP BY
        teacher_id
)

SELECT
    A.grade,
    CAST(COUNT(*) AS INTEGER) AS count
FROM
    assignments A
JOIN
    GradingCounts GC ON A.teacher_id = GC.teacher_id
WHERE
    A.grade = 'A' AND GC.grading_count = (
        SELECT MAX(grading_count) FROM GradingCounts
    )
GROUP BY
    A.grade;
