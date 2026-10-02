USE branch_mis_db;

CREATE VIEW vw_branch_transactions AS
SELECT
    t.transaction_id,
    t.transaction_date,
    t.year,
    t.month,
    t.quarter,
    t.`year_month`,
    t.transaction_type,
    t.transaction_media,
    t.transaction_amount,
    t.is_inflow,

    a.account_type,
    a.account_status,
    a.is_casa,
    a.opening_balance,

    b.branch_id,
    b.indian_state,
    b.region,
    b.zone,
    b.branch_type,

    c.age_group,
    c.occupation

FROM fact_transactions t

JOIN dim_accounts a
    ON a.account_id = t.account_id

JOIN dim_branches b
    ON b.branch_id = a.branch_id

JOIN dim_customers c
    ON c.customer_id = a.customer_id;
    
SELECT 
    *
FROM
    vw_branch_transactions
LIMIT 10;    

CREATE VIEW vw_target_vs_actual AS
SELECT
    bps.*,

    b.indian_state,
    b.region,
    b.zone,
    b.branch_type,

    ROUND(
        bps.actual_txn_amount - bps.target_txn_amount,
        2
    ) AS amount_gap

FROM branch_performance_summary bps

JOIN dim_branches b
    ON b.branch_id = bps.branch_id;

SELECT *
FROM vw_target_vs_actual
LIMIT 10;

SELECT * FROM vw_branch_transactions LIMIT 10;


