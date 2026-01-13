-- Source - https://codereview.stackexchange.com/q
-- Posted by nhgrif, modified by community. See post 'Timeline' for change history
-- Retrieved 2025-11-30, License - CC BY-SA 3.0

WITH Numbers AS (
    SELECT 1 as Number
    UNION ALL
    SELECT Number+1 FROM Numbers WHERE Number < 100
)
SELECT CASE
    WHEN Number % 15 = 0 THEN 'FizzBuzz'
    WHEN Number % 5 = 0 THEN 'Buzz'
    WHEN Number % 3 = 0 THEN 'Fizz'
    ELSE CAST(Number as varchar)
END AS FizzBuzz
FROM Numbers;
