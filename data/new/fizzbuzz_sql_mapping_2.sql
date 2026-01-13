-- Source - https://codereview.stackexchange.com/a
-- Posted by 200_success
-- Retrieved 2025-11-30, License - CC BY-SA 3.0

WITH R4 AS (
    SELECT col FROM (VALUES (1), (2), (3), (4)) x(col)
), R16 AS (
    SELECT a.col
        FROM R4 AS a CROSS JOIN R4 AS b
), R100 AS (
    SELECT TOP 100 ROW_NUMBER() OVER (ORDER BY a.col) AS n
        FROM R16 AS a CROSS JOIN R16 AS b
)
SELECT CASE
        WHEN n % 15 = 0 THEN 'FizzBuzz'
        WHEN n %  3 = 0 THEN 'Fizz'
        WHEN n %  5 = 0 THEN 'Buzz'
        ELSE CAST(n AS NVARCHAR(8))
       END AS FizzBuzz
    FROM R100
    ORDER BY n;
