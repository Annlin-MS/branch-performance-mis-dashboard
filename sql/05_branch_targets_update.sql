SELECT
    branch_id,
    year,
    month,
    actual_txn_amount,
    target_txn_amount,
    achievement_pct,
    performance_status
FROM vw_target_vs_actual
WHERE branch_id = 'B00001'
ORDER BY year, month;

SELECT
    performance_status,
    COUNT(*) AS record_count
FROM vw_target_vs_actual
WHERE year IN (2022, 2023)
GROUP BY performance_status;

SELECT
    MIN(achievement_pct) AS min_achievement,
    MAX(achievement_pct) AS max_achievement,
    AVG(achievement_pct) AS avg_achievement,
    COUNT(*) AS total_records
FROM vw_target_vs_actual
WHERE year IN (2022, 2023);

SELECT
    branch_id,
    year,
    month,
    actual_txn_amount,
    target_txn_amount,
    ROUND(
        actual_txn_amount / NULLIF(target_txn_amount, 0) * 100,
        2
    ) AS recalculated_achievement
FROM branch_performance_summary
WHERE year = 2022
  AND month = 1
ORDER BY recalculated_achievement DESC
LIMIT 10;

SELECT
    branch_id,
    target_year,
    target_month,
    target_txn_amount
FROM branch_targets
WHERE branch_id = 'B00021'
ORDER BY target_year, target_month
LIMIT 12;

SELECT
    a.branch_id,
    t.year,
    t.month,
    SUM(t.transaction_amount) AS actual_txn_amount
FROM fact_transactions t
JOIN dim_accounts a
    ON t.account_id = a.account_id
WHERE a.branch_id = 'B00021'
  AND t.year IN (2022, 2023)
GROUP BY
    a.branch_id,
    t.year,
    t.month
ORDER BY
    t.year,
    t.month;
    
SELECT
    a.branch_id,
    SUM(t.transaction_amount) AS total_txn_amount,
    SUM(t.transaction_amount) / 10 AS annual_average,
    (SUM(t.transaction_amount) / 10) / 12 AS monthly_average
FROM fact_transactions t
JOIN dim_accounts a
    ON t.account_id = a.account_id
WHERE a.branch_id = 'B00021'
GROUP BY a.branch_id;    

USE branch_mis_db;

SELECT COUNT(*) AS current_target_rows
FROM branch_targets;

DESCRIBE branch_targets;

SELECT COUNT(*) AS current_target_rows
FROM branch_targets;

CREATE TABLE branch_targets_backup_20261012
LIKE branch_targets;

INSERT INTO branch_targets_backup_20261012
SELECT * FROM branch_targets;

SELECT COUNT(*) AS backup_rows
FROM branch_targets_backup_20261012;

USE branch_mis_db;

CREATE TABLE branch_targets_staging (
    branch_id VARCHAR(10),
    target_year INT,
    target_month INT,
    target_txn_amount DECIMAL(15,2),
    target_loan_amount DECIMAL(15,2),
    target_new_accounts INT
);

SELECT COUNT(*) AS staging_rows
FROM branch_targets_staging;

SELECT *
FROM branch_targets_staging
WHERE branch_id = 'B00021'
  AND target_year = 2022
  AND target_month = 1;
  
SELECT COUNT(*) AS staging_rows
FROM branch_targets_staging;

SELECT *
FROM branch_targets_staging
WHERE branch_id = 'B00021'
  AND target_year = 2022
  AND target_month = 1;
  
SELECT COUNT(*) AS staging_rows
FROM branch_targets_staging;  

CREATE TABLE IF NOT EXISTS branch_targets_staging (
    branch_id VARCHAR(10),
    target_year INT,
    target_month INT,
    target_txn_amount DECIMAL(15,2),
    target_loan_amount DECIMAL(15,2),
    target_new_accounts INT
);


SELECT DATABASE() AS current_database;

SHOW TABLES LIKE 'branch_targets%';

SELECT COUNT(*) AS original_rows
FROM branch_targets;

SELECT COUNT(*) AS staging_rows
FROM branch_targets_staging;

SELECT *
FROM branch_targets_staging
WHERE branch_id = 'B00021'
  AND target_year = 2022
  AND target_month = 1;
  
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT CONCAT(
        branch_id, '-', target_year, '-', target_month
    )) AS unique_branch_months
FROM branch_targets_staging;  
  

USE branch_mis_db;

START TRANSACTION;

DELETE FROM branch_targets;

INSERT INTO branch_targets (
    branch_id,
    target_year,
    target_month,
    target_txn_amount,
    target_loan_amount,
    target_new_accounts
)
SELECT
    branch_id,
    target_year,
    target_month,
    target_txn_amount,
    target_loan_amount,
    target_new_accounts
FROM branch_targets_staging;

SELECT COUNT(*) AS updated_target_rows
FROM branch_targets;

COMMIT;
  
SELECT
    branch_id,
    target_year,
    target_month,
    target_txn_amount,
    target_loan_amount
FROM branch_targets
WHERE branch_id = 'B00021'
  AND target_year = 2022
  AND target_month = 1;  
  
DELIMITER $$

CREATE PROCEDURE recalculate_all_months()
BEGIN
    DECLARE v_year INT DEFAULT 2022;
    DECLARE v_month INT;

    WHILE v_year <= 2023 DO
        SET v_month = 1;

        WHILE v_month <= 12 DO
            CALL calculate_branch_performance(v_year, v_month);
            SET v_month = v_month + 1;
        END WHILE;

        SET v_year = v_year + 1;
    END WHILE;
END$$

DELIMITER ;

CALL recalculate_all_months();

DROP PROCEDURE recalculate_all_months;  

SELECT COUNT(*) AS summary_rows
FROM branch_performance_summary;

SELECT *
FROM branch_performance_summary
LIMIT 5;

SELECT
    MIN(year) AS first_year,
    MAX(year) AS last_year,
    COUNT(DISTINCT branch_id) AS branches,
    COUNT(DISTINCT CONCAT(year, '-', month)) AS year_months
FROM branch_performance_summary;


SELECT
    year,
    month,
    COUNT(*) AS branch_rows
FROM branch_performance_summary
GROUP BY year, month
ORDER BY year, month

SELECT
    year,
    month,
    COUNT(*) AS branch_rows
FROM branch_performance_summary
GROUP BY year, month
ORDER BY year, month;

SHOW CREATE PROCEDURE calculate_branch_performance;


USE branch_mis_db;

SELECT
    b.branch_id,
    b.indian_state
FROM dim_branches b
LEFT JOIN (
    SELECT DISTINCT a.branch_id
    FROM fact_transactions t
    JOIN dim_accounts a
        ON a.account_id = t.account_id
    WHERE t.year = 2022
      AND t.month = 1
) active_branches
    ON b.branch_id = active_branches.branch_id
WHERE active_branches.branch_id IS NULL
ORDER BY b.branch_id

DESCRIBE fact_loans;

