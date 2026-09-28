CREATE DATABASE branch_mis_db;
USE branch_mis_db;
show databases;

-- Create branch dimension
CREATE TABLE dim_branches (
    branch_id VARCHAR(10) PRIMARY KEY,
    branch_name VARCHAR(60),
    indian_state VARCHAR(60),
    region VARCHAR(20),
    zone VARCHAR(30),
    branch_type VARCHAR(20)
);

-- Check table structure
DESCRIBE dim_branches;

-- Create customer dimension
CREATE TABLE dim_customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    full_name VARCHAR(100),
    city VARCHAR(60),
    occupation VARCHAR(60),
    dob DATE,
    age INT,
    age_group VARCHAR(15)
);

-- Create account dimension
CREATE TABLE dim_accounts (
    account_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10),
    branch_id VARCHAR(10),
    opening_balance DECIMAL(15,2),
    account_open_date DATE,
    open_year INT,
    open_month INT,
    account_type VARCHAR(20),
    account_status VARCHAR(15),
    is_casa TINYINT(1),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (branch_id) REFERENCES dim_branches(branch_id)
);

-- Create indexes
CREATE INDEX idx_acc_branch ON dim_accounts(branch_id);
CREATE INDEX idx_acc_type ON dim_accounts(account_type);

-- Create transaction fact table
CREATE TABLE fact_transactions (
    transaction_id VARCHAR(10) PRIMARY KEY,
    account_id VARCHAR(10),
    transaction_date DATE,
    year INT,
    month INT,
    quarter VARCHAR(5),
    `year_month` VARCHAR(8),
    transaction_media VARCHAR(20),
    transaction_type VARCHAR(20),
    transaction_amount DECIMAL(15,2),
    is_inflow TINYINT(1),
    FOREIGN KEY (account_id) REFERENCES dim_accounts(account_id)
);

-- Create indexes
CREATE INDEX idx_txn_date ON fact_transactions(transaction_date);
CREATE INDEX idx_txn_yr_mth ON fact_transactions(`year_month`);
CREATE INDEX idx_txn_acct ON fact_transactions(account_id);

-- Create loan fact table
CREATE TABLE fact_loans (
    loan_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10),
    branch_id VARCHAR(10),
    loan_amount DECIMAL(15,2),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
    FOREIGN KEY (branch_id) REFERENCES dim_branches(branch_id)
);

-- Create branch targets table
CREATE TABLE branch_targets (
    target_id INT AUTO_INCREMENT PRIMARY KEY,
    branch_id VARCHAR(10),
    target_year INT,
    target_month INT,
    target_txn_amount DECIMAL(15,2),
    target_loan_amount DECIMAL(15,2),
    target_new_accounts INT,
    FOREIGN KEY (branch_id) REFERENCES dim_branches(branch_id)
);

-- Create branch performance summary table
CREATE TABLE branch_performance_summary (
    summary_id INT AUTO_INCREMENT PRIMARY KEY,
    calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    branch_id VARCHAR(10),
    year INT,
    month INT,
    actual_txn_amount DECIMAL(15,2),
    actual_txn_count INT,
    actual_inflow DECIMAL(15,2),
    actual_outflow DECIMAL(15,2),
    active_accounts INT,
    casa_accounts INT,
    casa_ratio DECIMAL(5,2),
    total_loan_amount DECIMAL(15,2),
    target_txn_amount DECIMAL(15,2),
    achievement_pct DECIMAL(6,2),
    performance_status VARCHAR(15),
    FOREIGN KEY (branch_id) REFERENCES dim_branches(branch_id)
);

show tables;
select database();


