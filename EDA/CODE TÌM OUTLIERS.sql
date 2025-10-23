-- Outlier theo log-IQR cho INWEEK
WITH base AS (
  SELECT
    CAST(Price_Inweek AS float) AS price,
    LOG10(CAST(Price_Inweek AS float)) AS lp
  FROM dbo.INWEEK
  WHERE Price_Inweek IS NOT NULL AND Price_Inweek > 0
),
f AS (  -- q1, q3 trên log-price
  SELECT TOP (1)
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY lp) OVER() AS q1,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY lp) OVER() AS q3
  FROM base
)
SELECT i.*
FROM dbo.INWEEK i
CROSS JOIN f
WHERE i.Price_Inweek > 0
  AND (
        LOG10(CAST(i.Price_Inweek AS float)) < f.q1 - 1.5*(f.q3 - f.q1)
     OR LOG10(CAST(i.Price_Inweek AS float)) > f.q3 + 1.5*(f.q3 - f.q1)
  )
ORDER BY i.Price_Inweek;


WITH base AS (
  SELECT
    CAST(Price_Weekend AS float) AS price,
    LOG10(CAST(Price_Weekend AS float)) AS lp
  FROM dbo.WEEKEND
  WHERE Price_Weekend IS NOT NULL AND Price_Weekend > 0
),
f AS (
  SELECT TOP (1)
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY lp) OVER() AS q1,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY lp) OVER() AS q3
  FROM base
)
SELECT w.*
FROM dbo.WEEKEND w
CROSS JOIN f
WHERE w.Price_Weekend > 0
  AND (
        LOG10(CAST(w.Price_Weekend AS float)) < f.q1 - 1.5*(f.q3 - f.q1)
     OR LOG10(CAST(w.Price_Weekend AS float)) > f.q3 + 1.5*(f.q3 - f.q1)
  )
ORDER BY w.Price_Weekend;
