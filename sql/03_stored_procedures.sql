USE branch_mis_db;

DELIMITER //

CREATE PROCEDURE calculate_branch_performance(
    IN p_year INT,
    IN p_month INT
)
BEGIN

    -- Remove existing calculation
    DELETE FROM branch_performance_summary
    WHERE year = p_year
      AND month = p_month;

    -- Calculate branch performance
    INSERT INTO branch_performance_summary (
        branch_id,
        year,
        month,
        actual_txn_amount,
        actual_txn_count,
        actual_inflow,
        actual_outflow,
        active_accounts,
        casa_accounts,
        casa_ratio,
        total_loan_amount,
        target_txn_amount,
        achievement_pct,
        performance_status
    )
    SELECT
        a.branch_id,
        p_year,
        p_month,

        ROUND(SUM(t.transaction_amount), 2),

        COUNT(t.transaction_id),

        ROUND(
            SUM(
                CASE
                    WHEN t.is_inflow = 1
                    THEN t.transaction_amount
                    ELSE 0
                END
            ), 2
        ),

        ROUND(
            SUM(
                CASE
                    WHEN t.is_inflow = 0
                    THEN t.transaction_amount
                    ELSE 0
                END
            ), 2
        ),

        COUNT(DISTINCT a.account_id),

        SUM(a.is_casa),

        ROUND(
            SUM(a.is_casa) * 100.0 /
            NULLIF(COUNT(DISTINCT a.account_id), 0),
            2
        ),

        COALESCE(
            (
                SELECT SUM(l.loan_amount)
                FROM fact_loans l
                WHERE l.branch_id = a.branch_id
            ),
            0
        ),

        COALESCE(bt.target_txn_amount, 0),

        ROUND(
            SUM(t.transaction_amount) * 100.0 /
            NULLIF(bt.target_txn_amount, 0),
            2
        ),

        CASE
            WHEN SUM(t.transaction_amount) >= bt.target_txn_amount
                THEN 'Achieved'
            WHEN SUM(t.transaction_amount) >= bt.target_txn_amount * 0.85
                THEN 'At Risk'
            ELSE 'Missed'
        END

    FROM fact_transactions t

    JOIN dim_accounts a
        ON a.account_id = t.account_id

    LEFT JOIN branch_targets bt
        ON bt.branch_id = a.branch_id
        AND bt.target_year = p_year
        AND bt.target_month = p_month

    WHERE t.year = p_year
      AND t.month = p_month

    GROUP BY
        a.branch_id,
        bt.target_txn_amount;

    SELECT CONCAT(
        'Done: ',
        p_year,
        '-',
        LPAD(p_month, 2, '0')
    ) AS result;

END //

DELIMITER ;

SHOW PROCEDURE STATUS
WHERE Db = 'branch_mis_db';

CALL calculate_branch_performance(2022, 1);

SELECT *
FROM branch_performance_summary
WHERE year = 2022
  AND month = 1
LIMIT 10;