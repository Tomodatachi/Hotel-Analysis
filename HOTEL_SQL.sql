1)
-- View Table of hotels
SELECT * FROM cleaned_bookings

-- View how many hotels are there in the table
SELECT COUNT(*) as total_rows FROM cleaned_bookings;

2)
-- Check null hotels.
SELECT 
    COUNT(*) - COUNT(Name) as null_name,
    COUNT(*) - COUNT(Price_2_Adultsnight) as null_price,
    COUNT(*) - COUNT(score) as Score
FROM cleaned_bookings;

SELECT 
    ROUND(100.0 * (COUNT(*) - COUNT(Name)) / COUNT(*), 2) as null_percentage
FROM cleaned_bookings;

-- Find hotels with NULL prices
SELECT * FROM cleaned_bookings 
WHERE Price_2_Adultsnight IS NULL;

3)
SELECT 
    COUNT(score) as count,
    MIN(score) as min_value,
    MAX(score) as max_value,
    AVG(score) as mean,
    STDEV(score) as std_dev,
    VAR(score) as variance
FROM cleaned_bookings;

SELECT
(
 (SELECT MAX(Score) FROM
   (SELECT TOP 50 PERCENT Score FROM cleaned_bookings ORDER BY Score) AS BottomHalf)
 +
 (SELECT MIN(Score) FROM
   (SELECT TOP 50 PERCENT Score FROM cleaned_bookings ORDER BY Score DESC) AS TopHalf)
) / 2 AS Median

SELECT 
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Score) OVER (PARTITION BY Name) as Q1,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY Score) OVER (PARTITION BY Name) as median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Score) OVER (PARTITION BY Name) as Q3
FROM cleaned_bookings;

4)
--- Count how many types of rankings
SELECT COUNT(DISTINCT overall) as unique_count
FROM cleaned_bookings;

-- Count how many hotels based on each type
SELECT
    overall,
    COUNT(*) as frequency,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cleaned_bookings), 2) as percentage
FROM cleaned_bookings
GROUP BY overall
ORDER BY frequency DESC;

--TOP 10 popular scores
SELECT TOP 10 score, COUNT(*) as count
FROM cleaned_bookings
GROUP BY score
ORDER BY count DESC

5)
-- Find outliers in score
WITH stats AS (
    SELECT 
        AVG(score) as mean_val,
        STDEV(score) as std_val
    FROM cleaned_bookings
)
SELECT *,
    ABS((score - mean_val) / std_val) as z_score
FROM cleaned_bookings, stats
WHERE ABS((score - mean_val) / std_val) > 3;

6)
-- find duplicates
SELECT *, COUNT(*) as duplicate_count
FROM cleaned_bookings
GROUP BY Name, Province, Price_2_Adultsnight, Check_in, Check_out, score, stars, address, reviews, overall, link  -- tất cả các cột
HAVING COUNT(*) > 1;


7)
-- Count Hotels by province
SELECT Province, COUNT(*) as count
FROM cleaned_bookings
GROUP BY Province
ORDER BY Province;

-- AVG price between provinces
SELECT 
    Province,
    AVG(Price_2_Adultsnight) as avg_value,
    COUNT(*) as count
FROM cleaned_bookings
GROUP BY Province
ORDER BY avg_value DESC;

8)
SELECT 
    DATETRUNC(month, Check_in) as month,
    COUNT(*) as count,
    AVG(Price_2_Adultsnight) as avg_value
FROM cleaned_bookings
GROUP BY DATETRUNC(month, Check_in)
ORDER BY month;

9)
--FIND INVALID SCORES, PRICES:
SELECT * FROM cleaned_bookings
WHERE Price_2_Adultsnight < 0 OR score > 10 OR score < 0;


--FIND INVALID DATES
SELECT * FROM cleaned_bookings
WHERE Check_in > Check_out;  



