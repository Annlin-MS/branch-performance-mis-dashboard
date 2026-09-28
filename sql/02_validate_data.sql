SHOW VARIABLES LIKE 'local_infile';
USE branch_mis_db;

SELECT 'Branches' AS table_name, COUNT(*) AS row_count
FROM dim_branches

UNION ALL

SELECT 'Customers', COUNT(*)
FROM dim_customers

UNION ALL

SELECT 'Accounts', COUNT(*)
FROM dim_accounts

UNION ALL

SELECT 'Transactions', COUNT(*)
FROM fact_transactions

UNION ALL

SELECT 'Loans', COUNT(*)
FROM fact_loans

UNION ALL

SELECT 'Branch Targets', COUNT(*)
FROM branch_targets;