--Xem toàn bộ data
SELECT *
FROM INWEEK I, WEEKEND W
WHERE I.Hotel_ID = W.Hotel_ID
--1) Quy mô dữ liệu theo bảng
SELECT 'INWEEK' AS 'TABLE' ,COUNT(*) AS 'ROWS'
FROM INWEEK 
UNION
SELECT 'WEEKEND' AS 'TABLE' ,COUNT(*) AS 'ROWS'
FROM WEEKEND
--Kiểm tra nhanh số dòng từng bảng, phát hiện mất mát dữ liệu hay sai lệch kích thước.

--2) KIỂM TRA GIÁ TRỊ NULL
SELECT
    'INWEEK' AS 'TABLE',
    COUNT(*) - COUNT(I.HOTEL_NAME) AS 'HOTEL_NAME',
    COUNT(*) - COUNT(PRICE_INWEEK) AS 'PRICE',
    COUNT(*) - COUNT(PROVINCE) AS 'PROVINCE',
    COUNT(*) - COUNT(CHECK_IN) AS 'CHECK_IN',
    COUNT(*) - COUNT(CHECK_OUT) AS 'CHECK_OUT',
    COUNT(*) - COUNT(SCORE) AS 'SCORE',
    COUNT(*) - COUNT(STARS) AS 'STARS',
    COUNT(*) - COUNT(ADDRESS) AS 'ADDRESS',
    COUNT(*) - COUNT(REVIEWS) AS 'REVIEWS',
    COUNT(*) - COUNT(OVERALL) AS 'OVERALL',
    COUNT(*) - COUNT(LINK) AS 'LINK'
FROM INWEEK I
UNION
SELECT
    'WEEKEND' AS 'TABLE',
    COUNT(*) - COUNT(HOTEL_NAME) AS 'HOTEL_NAME',
    COUNT(*) - COUNT(PRICE_WEEKEND) AS 'PRICE',
    COUNT(*) - COUNT(PROVINCE) AS 'PROVINCE',
    COUNT(*) - COUNT(CHECK_IN) AS 'CHECK_IN',
    COUNT(*) - COUNT(CHECK_OUT) AS 'CHECK_OUT',
    COUNT(*) - COUNT(SCORE) AS 'SCORE',
    COUNT(*) - COUNT(STARS) AS 'STARS',
    COUNT(*) - COUNT(ADDRESS) AS 'ADDRESS',
    COUNT(*) - COUNT(REVIEWS) AS 'REVIEWS',
    COUNT(*) - COUNT(OVERALL) AS 'OVERALL',
    COUNT(*) - COUNT(LINK) AS 'LINK'
FROM WEEKEND 

--3)THỐNG KÊ MÔ TẢ CHO GIÁ KHÁCH SẠN.
EXEC sp_rename 'DBO.WEEKEND.PRICE_2_ADULTS_NIGHT', 'Price_Weekend', 'COLUMN';

SELECT
    'INWEEK' AS 'TABLE',
    COUNT(PRICE_INWEEK) AS 'COUNT',
    AVG(PRICE_INWEEK) AS 'AVERAGE',
    MIN(PRICE_INWEEK) AS 'MIN',
    MAX(PRICE_INWEEK) AS 'MAX',
    VAR(PRICE_INWEEK) AS 'VARIANCE',
    STDEV(PRICE_INWEEK) AS 'STD'
FROM INWEEK
UNION
SELECT
    'WEEKEND' AS 'TABLE',
    COUNT(PRICE_WEEKEND) AS 'COUNT',
    AVG(PRICE_WEEKEND) AS 'AVERAGE',
    MIN(PRICE_WEEKEND) AS 'MIN',
    MAX(PRICE_WEEKEND) AS 'MAX',
    VAR(PRICE_WEEKEND) AS 'VARIANCE',
    STDEV(PRICE_WEEKEND) AS 'STD'
FROM WEEKEND

--TÌM TRUNG VỊ
SELECT DISTINCT
    'INWEEK' AS 'TABLE',
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY PRICE_INWEEK) OVER() as Q1,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY PRICE_INWEEK) OVER() as median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY PRICE_INWEEK) OVER() as Q3
FROM INWEEK
UNION
SELECT DISTINCT
    'WEEKEND' AS 'TABLE',
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY PRICE_WEEKEND) OVER() as Q1,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY PRICE_WEEKEND) OVER() as median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY PRICE_WEEKEND) OVER() as Q3
FROM WEEKEND


--4) Phân phối mức sao theo tỉnh
SELECT Province,
       SUM(CASE WHEN Stars=5 THEN 1 ELSE 0 END) AS s5,
       SUM(CASE WHEN Stars=4 THEN 1 ELSE 0 END) AS s4,
       SUM(CASE WHEN Stars=3 THEN 1 ELSE 0 END) AS s3,
       SUM(CASE WHEN Stars=2 THEN 1 ELSE 0 END) AS s2,
       SUM(CASE WHEN Stars=1 THEN 1 ELSE 0 END) AS s1,
       SUM(CASE WHEN Stars=0 THEN 1 ELSE 0 END) AS s0,
       SUM(CASE WHEN Stars IS NULL THEN 1 ELSE 0 END) AS s_unknown
FROM WEEKEND
GROUP BY Province
ORDER BY Province;
--Mục đích: Cấu trúc chất lượng cơ sở lưu trú theo khu vực (tỷ trọng sao).


--5)Đếm số tỉnh và tần suất từng tỉnh
SELECT 
    Province,
    COUNT(*) AS hotel_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM dbo.INWEEK), 2) AS percentage
FROM dbo.INWEEK
GROUP BY Province
ORDER BY hotel_count DESC;
--6) Xếp hạng tỉnh theo giá trung bình (WEEKEND)
SELECT Province,
       COUNT(*) AS 'NUMBER_OF_HOTEL',
       AVG(Price_2_adults_night) AS avg_price
FROM WEEKEND
GROUP BY Province
HAVING COUNT(*) >= 20      -- ngưỡng tối thiểu mẫu, tùy chỉnh
ORDER BY avg_price DESC;
--Tỉnh nào có mặt bằng giá cao/thấp (lọc tỉnh ít mẫu để tránh nhiễu).

--7) Top 5 khách sạn đắt nhất theo tỉnh 
WITH RankedHotels AS (
    SELECT 
        Province,
        Hotel_ID,
        Hotel_Name,
        Price_Inweek,
        Stars,
        Score,
        ROW_NUMBER() OVER (
            PARTITION BY Province 
            ORDER BY Price_Inweek DESC
        ) AS RANKED
    FROM dbo.INWEEK
    WHERE Price_Inweek IS NOT NULL
)
SELECT 
    Province,
    Hotel_ID,
    Hotel_Name,
    Stars,
    Score,
    Price_Inweek
FROM RankedHotels
WHERE RANKED <= 5
ORDER BY Province
--8) Đếm số lượng sao
SELECT Stars, COUNT(*) AS 'HOTEL'
FROM dbo.INWEEK
GROUP BY Stars
ORDER BY Stars;
--9)PHÁT HIỆN OUTLIERS
WITH stats AS (
    SELECT DISTINCT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Price_Inweek) OVER() AS Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Price_Inweek) OVER() AS Q3
    FROM INWEEK
)
SELECT i.*
FROM INWEEK i
CROSS JOIN (SELECT Q1, Q3 FROM stats) s
WHERE Price_Inweek < (Q1 - 1.5*(Q3 - Q1))
   OR Price_Inweek > (Q3 + 1.5*(Q3 - Q1))
ORDER BY Price_Inweek;
--10) PHÁT HIỆN KHÁCH SẠN TRÙNG LẶP
SELECT Hotel_ID, Hotel_Name, COUNT(*) AS dup_count
FROM INWEEK
GROUP BY Hotel_ID, Hotel_Name
HAVING COUNT(*) > 1
ORDER BY dup_count DESC;
--11)PHÂN TÍCH TƯƠNG QUAN GIÁ, SAO, ĐIỂM
SELECT Stars,
       COUNT(*) AS n,
       AVG(Price_Inweek) AS avg_price,
       AVG(Score) AS avg_score
FROM dbo.INWEEK
GROUP BY Stars
ORDER BY Stars;

--12) So sánh giá cuối tuần vs trong tuần
SELECT 
    i.Hotel_ID,
    i.Hotel_Name,
    i.Province,
    i.Price_Inweek,
    w.Price_Weekend,
    (w.Price_Weekend - i.Price_Inweek) AS diff_price
FROM dbo.INWEEK i
JOIN dbo.WEEKEND w ON i.Hotel_ID = w.Hotel_ID
ORDER BY diff_price DESC;
--Mục đích: Đo “phí premium” cuối tuần 

--13) Phân bổ “bucket” giá (WEEKEND)
WITH base AS (
  SELECT Price_Weekend AS p
  FROM WEEKEND
)
SELECT CASE
         WHEN p < 300000 THEN '<300k'
         WHEN p < 600000 THEN '300k–600k'
         WHEN p < 1000000 THEN '600k–1m'
         WHEN p < 1500000 THEN '1m–1.5m'
         WHEN p < 2500000 THEN '1.5m–2.5m'
         ELSE '>=2.5m'
       END AS price_bucket,
       COUNT(*) AS n
FROM base
GROUP BY CASE
         WHEN p < 300000 THEN '<300k'
         WHEN p < 600000 THEN '300k–600k'
         WHEN p < 1000000 THEN '600k–1m'
         WHEN p < 1500000 THEN '1m–1.5m'
         WHEN p < 2500000 THEN '1.5m–2.5m'
         ELSE '>=2.5m'
       END
ORDER BY MIN(p);

--14)TÍNH TƯƠNG QUAN GIỮA STAR VÀ PRICE
WITH base AS (
  SELECT CAST(Stars AS float) AS x, CAST(Price_Inweek AS float) AS y
  FROM dbo.INWEEK
  WHERE Stars IS NOT NULL AND Price_Inweek IS NOT NULL
),
agg AS (
  SELECT COUNT(*) AS n, AVG(x) AS mx, AVG(y) AS my,
         AVG(x*y) AS mxy, AVG(x*x) AS mxx, AVG(y*y) AS myy
  FROM base
)
SELECT (mxy - mx*my) / (SQRT(mxx - mx*mx) * SQRT(myy - my*my)) AS corr_stars_price
FROM agg;

--15)Corr Stars–Price theo Province
WITH b AS (
  SELECT Province, CAST(Stars AS float) x, CAST(Price_Inweek AS float) y
  FROM dbo.INWEEK WHERE Stars IS NOT NULL AND Price_Inweek IS NOT NULL
), a AS (
  SELECT Province, COUNT(*) n, AVG(x) mx, AVG(y) my,
         AVG(x*y) mxy, AVG(x*x) mxx, AVG(y*y) myy
  FROM b GROUP BY Province
)
SELECT Province,
       (mxy - mx*my) / NULLIF(SQRT(mxx - mx*mx)*SQRT(myy - my*my),0) AS corr
FROM a ORDER BY corr DESC;

--16) Tóm tắt điểm đánh giá và số review (WEEKEND) theo tỉnh và số sao
SELECT Province, Stars,
       AVG(Score) AS avg_score,
       MIN(Score) AS min_score,
       MAX(Score) AS max_score,
       AVG(TRY_CONVERT(FLOAT, Reviews)) AS avg_reviews
FROM WEEKEND
GROUP BY Province, Stars
ORDER BY Province, Stars;


--17) Phân phối nhãn Overall (WEEKEND)
SELECT Overall, COUNT(*) AS 'COUNT'
FROM WEEKEND
GROUP BY Overall
ORDER BY 'COUNT' DESC;

--18) Khách sạn “bất thường”: điểm cao nhưng review thấp (WEEKEND)
SELECT Hotel_ID, Hotel_Name, Province, Score, Reviews
FROM WEEKEND
WHERE Score >= 9.0 AND TRY_CONVERT(INT, Reviews) < 20
ORDER BY Score DESC, TRY_CONVERT(INT, Reviews);
--Điểm rất cao nhưng số review ít → có thể là khách sạn mới

--19) Khách sạn “rủi ro”: điểm thấp nhưng giá cao (WEEKEND)
SELECT TOP 20 Hotel_ID, Hotel_Name, Province, Stars, Score, Price_Weekend
FROM WEEKEND
ORDER BY Score ASC, Price_Weekend DESC;



--20) Sự khác biệt giá INWEEK vs WEEKEND theo sao (tổng quát)
WITH wkd AS (
  SELECT Stars, AVG(Price_Weekend) AS weekend_price
  FROM WEEKEND
  GROUP BY Stars
),
wkdy AS (
  SELECT Stars, AVG(Price_Inweek) AS inweek_price
  FROM INWEEK
  GROUP BY Stars
)
SELECT COALESCE(wkd.Stars, wkdy.Stars) AS Stars,
       wkd.weekend_price, wkdy.inweek_price,
       (wkd.weekend_price - wkdy.inweek_price) AS premium_weekend
FROM wkd
FULL OUTER JOIN wkdy ON wkd.Stars = wkdy.Stars
ORDER BY Stars;
--Mục đích: Nhìn theo phân khúc sao, cuối tuần đội giá bao nhiêu so với trong tuần.