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

DELIMITER //

CREATE PROCEDURE get_branch_ranking(
    IN p_year INT
)
BEGIN

    SELECT
        b.branch_id,
        b.indian_state,
        b.region,
        b.zone,

        SUM(t.transaction_amount) AS total_txn_amount,

        COUNT(t.transaction_id) AS total_txn_count,

        SUM(l.loan_amount) AS total_loan_amount,

        COUNT(DISTINCT a.account_id) AS total_accounts,

        -- Overall branch ranking
        RANK() OVER (
            ORDER BY SUM(t.transaction_amount) DESC
        ) AS txn_rank,

        -- Ranking within region
        RANK() OVER (
            PARTITION BY b.region
            ORDER BY SUM(t.transaction_amount) DESC
        ) AS region_rank,

        -- Running transaction total
        ROUND(
            SUM(SUM(t.transaction_amount)) OVER (
                ORDER BY SUM(t.transaction_amount) DESC
                ROWS BETWEEN UNBOUNDED PRECEDING
                AND CURRENT ROW
            ),
            2
        ) AS running_total

    FROM fact_transactions t

    JOIN dim_accounts a
        ON a.account_id = t.account_id

    JOIN dim_branches b
        ON b.branch_id = a.branch_id

    LEFT JOIN fact_loans l
        ON l.branch_id = b.branch_id

    WHERE t.year = p_year

    GROUP BY
        b.branch_id,
        b.indian_state,
        b.region,
        b.zone

    ORDER BY txn_rank;

END //

DELIMITER ;

SHOW PROCEDURE STATUS
WHERE Db = 'branch_mis_db';

CALL get_branch_ranking(2023);

DELIMITER //

CREATE PROCEDURE get_monthly_trend(
    IN p_year INT
)
BEGIN

    WITH monthly_data AS (
        SELECT
            b.branch_id,
            b.indian_state,
            b.region,
            t.month,
            t.`year_month`,
            SUM(t.transaction_amount) AS monthly_amount,
            COUNT(t.transaction_id) AS monthly_count,
            SUM(t.is_inflow) AS deposit_count

        FROM fact_transactions t

        JOIN dim_accounts a
            ON a.account_id = t.account_id

        JOIN dim_branches b
            ON b.branch_id = a.branch_id

        WHERE t.year = p_year

        GROUP BY
            b.branch_id,
            b.indian_state,
            b.region,
            t.month,
            t.`year_month`
    )

    SELECT
        branch_id,
        indian_state,
        region,
        month,
        `year_month`,
        monthly_amount,
        monthly_count,

        LAG(monthly_amount) OVER (
            PARTITION BY branch_id
            ORDER BY month
        ) AS prev_month_amount,

        ROUND(
            (
                monthly_amount -
                LAG(monthly_amount) OVER (
                    PARTITION BY branch_id
                    ORDER BY month
                )
            )
            /
            NULLIF(
                LAG(monthly_amount) OVER (
                    PARTITION BY branch_id
                    ORDER BY month
                ),
                0
            ) * 100,
            2
        ) AS mom_growth_pct

    FROM monthly_data

    ORDER BY branch_id, month;

END //

DELIMITER ;

CALL get_monthly_trend(2023);

DELIMITER //

CREATE PROCEDURE get_casa_analysis()
BEGIN

    SELECT
        b.indian_state,
        b.region,

        COUNT(a.account_id) AS total_accounts,

        SUM(
            CASE
                WHEN a.account_type IN ('Savings', 'Checking')
                THEN 1
                ELSE 0
            END
        ) AS casa_count,

        SUM(
            CASE
                WHEN a.account_type = 'Fixed Deposit'
                THEN 1
                ELSE 0
            END
        ) AS fd_count,

        ROUND(
            SUM(a.is_casa) * 100.0 /
            NULLIF(COUNT(a.account_id), 0),
            2
        ) AS casa_ratio_pct,

        SUM(a.opening_balance) AS total_opening_balance,

        SUM(
            CASE
                WHEN a.account_status = 'Active'
                THEN 1
                ELSE 0
            END
        ) AS active_accounts

    FROM dim_accounts a

    JOIN dim_branches b
        ON b.branch_id = a.branch_id

    GROUP BY
        b.indian_state,
        b.region

    ORDER BY
        casa_ratio_pct DESC;

END //

DELIMITER ;

CALL get_casa_analysis();



DELIMITER //

DROP PROCEDURE IF EXISTS get_transaction_channel_mix//

CREATE PROCEDURE get_transaction_channel_mix()
BEGIN

    SELECT
        b.branch_id,
        b.indian_state,
        b.region,
        t.transaction_media,

        COUNT(t.transaction_id) AS txn_count,

        SUM(t.transaction_amount) AS txn_amount,

        ROUND(
            COUNT(t.transaction_id) * 100.0 /
            SUM(COUNT(t.transaction_id)) OVER (
                PARTITION BY b.branch_id
            ),
            2
        ) AS pct_of_branch

    FROM fact_transactions t

    JOIN dim_accounts a
        ON a.account_id = t.account_id

    JOIN dim_branches b
        ON b.branch_id = a.branch_id

    GROUP BY
        b.branch_id,
        b.indian_state,
        b.region,
        t.transaction_media

    ORDER BY
        b.indian_state,
        b.branch_id,
        txn_amount DESC;

END //

DELIMITER ;

CALL get_transaction_channel_mix();