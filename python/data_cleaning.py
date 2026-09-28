import pandas as pd
import numpy as np

# Load the datasets
df_branch = pd.read_csv("../data/raw/Bank_Branch_Data.csv")
df_customer = pd.read_csv("../data/raw/Bank_Customer_Data.csv")
df_account = pd.read_csv("../data/raw/Bank_Account_Data.csv")
df_transaction = pd.read_csv("../data/raw/Bank_Transacation_Data.csv")
df_loan = pd.read_csv("../data/raw/Bank_Loan_Data.csv")

#check dataset dimensions
print(df_branch.shape)
print(df_customer.shape)
print(df_account.shape)
print(df_transaction.shape)
print(df_loan.shape)

# Display sample records
print(df_branch.head())
print(df_customer.head())
print(df_account.head())
print(df_transaction.head())
print(df_loan.head())

# Check columns
print(df_branch.columns)
print(df_customer.columns)
print(df_account.columns)
print(df_transaction.columns)
print(df_loan.columns)

# Map US states to Indian states
us_to_india = {
    'Alabama':'Kerala', 'Alaska':'Ladakh',
    'Arizona':'Rajasthan', 'Arkansas':'Chhattisgarh',
    'California':'Maharashtra', 'Colorado':'Uttarakhand',
    'Connecticut':'Goa', 'Delaware':'Puducherry',
    'District of Columbia':'New Delhi', 'Hawaii':'Andaman and Nicobar',
    'Idaho':'Himachal Pradesh', 'Illinois':'Uttar Pradesh',
    'Indiana':'Bihar', 'Iowa':'Odisha',
    'Kansas':'Madhya Pradesh', 'Kentucky':'Jharkhand',
    'Louisiana':'Andhra Pradesh', 'Maine':'Meghalaya',
    'Maryland':'Haryana', 'Massachusetts':'West Bengal',
    'Michigan':'Gujarat', 'Minnesota':'Punjab',
    'Mississippi':'Telangana', 'Missouri':'Assam',
    'Montana':'Arunachal Pradesh', 'Nebraska':'Manipur',
    'Nevada':'Jammu and Kashmir', 'New Hampshire':'Tripura',
    'New Jersey':'Tamil Nadu', 'New Mexico':'Nagaland',
    'New York':'Karnataka', 'North Carolina':'Sikkim',
    'North Dakota':'Mizoram', 'Ohio':'Delhi',
    'Oklahoma':'Uttarakhand', 'Oregon':'Himachal Pradesh',
    'Pennsylvania':'Madhya Pradesh', 'Puerto Rico':'Lakshadweep',
    'Rhode Island':'Dadra and NH', 'South Carolina':'Chandigarh',
    'South Dakota':'Meghalaya', 'Tennessee':'Tamil Nadu',
    'Texas':'Telangana', 'Utah':'Gujarat',
    'Vermont':'Sikkim', 'Virgin Islands':'Lakshadweep',
    'Virginia':'Kerala', 'Washington':'Maharashtra',
    'West Virginia':'Jharkhand', 'Wisconsin':'Karnataka',
    'Wyoming':'Rajasthan'
}

# Map states to regions
state_to_region = {
    'Kerala':'South', 'Karnataka':'South', 'Tamil Nadu':'South',
    'Andhra Pradesh':'South', 'Telangana':'South', 'Puducherry':'South',
    'Goa':'West', 'Maharashtra':'West', 'Gujarat':'West',
    'Dadra and NH':'West', 'Chandigarh':'North',
    'Rajasthan':'North', 'New Delhi':'North', 'Delhi':'North',
    'Haryana':'North', 'Punjab':'North', 'Uttarakhand':'North',
    'Himachal Pradesh':'North', 'Jammu and Kashmir':'North',
    'Ladakh':'North', 'Uttar Pradesh':'North',
    'Madhya Pradesh':'Central', 'Chhattisgarh':'Central',
    'Bihar':'East', 'Jharkhand':'East',
    'West Bengal':'East', 'Odisha':'East',
    'Assam':'Northeast', 'Arunachal Pradesh':'Northeast',
    'Manipur':'Northeast', 'Meghalaya':'Northeast',
    'Mizoram':'Northeast', 'Nagaland':'Northeast',
    'Tripura':'Northeast', 'Sikkim':'Northeast',
    'Andaman and Nicobar':'Island', 'Lakshadweep':'Island'
}

# Map regions to zones
state_to_type = {
    'South':'South Zone',
    'West':'West Zone',
    'North':'North Zone',
    'Central':'Central Zone',
    'East':'East Zone',
    'Northeast':'Northeast Zone',
    'Island':'Island Zone'
}

# Apply mapping to branch data
df_branch['INDIAN_STATE'] = df_branch['BRANCH_STATE'].map(us_to_india)
df_branch['REGION'] = df_branch['INDIAN_STATE'].map(state_to_region)
df_branch['ZONE'] = df_branch['REGION'].map(state_to_type)

# Create branch type
df_branch['BRANCH_TYPE'] = np.where(
    df_branch['REGION'].isin(['South', 'West', 'North']),
    'Urban',
    'Semi-Urban'
)

print('Branch file cleaned. Shape:', df_branch.shape)

# Convert DOB to datetime
df_customer['DOB'] = pd.to_datetime(df_customer['DOB'], errors='coerce')

# Calculate age
df_customer['AGE'] = 2024 - df_customer['DOB'].dt.year

# Create age groups
df_customer['AGE_GROUP'] = pd.cut(
    df_customer['AGE'],
    bins=[0, 25, 35, 50, 65, 120],
    labels=['Below 25', '25-35', '35-50', '50-65', '65+']
)

# Create full name
df_customer['FULL_NAME'] = (
    df_customer['First_Name'] + ' ' +
    df_customer['Last_Name']
)

# Check customer data
print(df_customer.head())
print(df_customer[['DOB', 'AGE', 'AGE_GROUP', 'FULL_NAME']].head())
print(df_customer.shape)

# Convert account open date
df_account['ACCOUNT_OPEN_DATE'] = pd.to_datetime(
    df_account['ACCOUNT_OPEN_DATE']
)

# Extract opening year
df_account['OPEN_YEAR'] = (
    df_account['ACCOUNT_OPEN_DATE'].dt.year
)

# Extract opening month
df_account['OPEN_MONTH'] = (
    df_account['ACCOUNT_OPEN_DATE'].dt.month
)

# Create CASA flag
df_account['IS_CASA'] = df_account['ACCOUNT_TYPE'].apply(
    lambda x: 1 if x in ['Savings', 'Checking'] else 0
)
# Check account data
print(df_account.head())

# Check CASA distribution
print(df_account['IS_CASA'].value_counts())

# Check dataset shape
print(df_account.shape)

# Standardize transaction column names
df_transaction.columns = [
    c.replace('TRANSCATION', 'TRANSACTION')
    for c in df_transaction.columns
]

# Convert transaction date
df_transaction['TRANSACTION_DATE'] = pd.to_datetime(
    df_transaction['TRANSACTION_DATE']
)

# Extract transaction year
df_transaction['YEAR'] = (
    df_transaction['TRANSACTION_DATE'].dt.year
)

# Extract transaction month
df_transaction['MONTH'] = (
    df_transaction['TRANSACTION_DATE'].dt.month
)

# Create quarter
df_transaction['QUARTER'] = (
    'Q' + df_transaction['TRANSACTION_DATE'].dt.quarter.astype(str)
)

# Create year-month field
df_transaction['YEAR_MONTH'] = (
    df_transaction['TRANSACTION_DATE']
    .dt.to_period('M')
    .astype(str)
)

# Create inflow flag
df_transaction['IS_INFLOW'] = (
    df_transaction['TRANSACTION_TYPE']
    .apply(lambda x: 1 if x == 'Deposit' else 0)
)

# Keep valid transaction amounts
df_transaction = df_transaction[
    df_transaction['TRANSACTION_AMOUNT'] > 0
]

# Check transaction data
print(df_transaction.head())

# Check dataset shape
print(df_transaction.shape)

# Check transaction types
print(df_transaction['TRANSACTION_TYPE'].value_counts())

# Check transaction media
print(df_transaction['TRANSACTION_MEDIA'].value_counts())

# Save cleaned datasets
df_branch.to_csv("../data/clean/clean_branches.csv", index=False)
df_customer.to_csv("../data/clean/clean_customers.csv", index=False)
df_account.to_csv("../data/clean/clean_accounts.csv", index=False)
df_transaction.to_csv("../data/clean/clean_transactions.csv", index=False)
df_loan.to_csv("../data/clean/clean_loans.csv", index=False)

# Join transactions with branch IDs
txn_acc = df_transaction.merge(
    df_account[['ACCOUNT_ID', 'BRANCH_ID']],
    on='ACCOUNT_ID'
)

# Calculate annual transaction amount by branch
branch_annual = (
    txn_acc.groupby('BRANCH_ID')['TRANSACTION_AMOUNT']
    .sum()
    .reset_index()
)

branch_annual.columns = [
    'BRANCH_ID',
    'ANNUAL_ACTUAL'
]

# Initialize target records
targets = []

# Generate monthly branch targets
for _, row in branch_annual.iterrows():
    monthly_base = row['ANNUAL_ACTUAL'] / 10

    for year in [2022, 2023]:
        for month in range(1, 13):
            targets.append({
                'BRANCH_ID': row['BRANCH_ID'],
                'TARGET_YEAR': year,
                'TARGET_MONTH': month,
                'TARGET_TXN_AMOUNT': round(monthly_base * 1.05, 2),
                'TARGET_LOAN_AMOUNT': round(monthly_base * 0.8, 2),
                'TARGET_NEW_ACCOUNTS': 15
            })

# Convert targets to DataFrame
targets_df = pd.DataFrame(targets)

# Save branch targets
targets_df.to_csv(
    "../data/clean/branch_targets.csv",
    index=False
)

# Display final file counts
print("=== ALL FILES SAVED ===")
print("clean_branches.csv ->", len(df_branch), "rows")
print("clean_customers.csv ->", len(df_customer), "rows")
print("clean_accounts.csv ->", len(df_account), "rows")
print("clean_transactions.csv ->", len(df_transaction), "rows")
print("clean_loans.csv ->", len(df_loan), "rows")
print("branch_targets.csv ->", len(targets_df), "rows")

# Check branch rows and unique branches
print(df_branch.shape)
print(df_branch['BRANCH_ID'].nunique())

# Keep one row per branch
df_branch = df_branch.drop_duplicates(subset=['BRANCH_ID'])

# Save cleaned branches
df_branch.to_csv("../data/clean/clean_branches.csv", index=False)

print(df_branch.shape)

# Check branch mapping
print(df_branch[['BRANCH_ID', 'BRANCH_STATE', 'INDIAN_STATE', 'REGION', 'ZONE']].head(10))

# Prepare branch data for MySQL
df_branch_mysql = df_branch[
    ['BRANCH_ID', 'BRANCH_NAME', 'INDIAN_STATE', 'REGION', 'ZONE', 'BRANCH_TYPE']
]

df_branch_mysql.to_csv(
    "../data/clean/clean_branches_mysql.csv",
    index=False
)

# Prepare customer data for MySQL
df_customer_mysql = df_customer[
    ['CUSTOMER_ID', 'FULL_NAME', 'City', 'Occupation', 'DOB', 'AGE', 'AGE_GROUP']
].copy()

# Rename columns to match MySQL
df_customer_mysql.columns = [
    'customer_id',
    'full_name',
    'city',
    'occupation',
    'dob',
    'age',
    'age_group'
]

df_customer_mysql.to_csv(
    "../data/clean/clean_customers_mysql.csv",
    index=False
)

print("Customer rows:", len(df_customer))
print("MySQL customer rows:", len(df_customer_mysql))

import pandas as pd

# Check saved customer CSV
check = pd.read_csv("../data/clean/clean_customers_mysql.csv")

print("CSV rows:", len(check))
print("CSV columns:", list(check.columns))

# Check customer ID relationships
print("Customers:", df_customer['CUSTOMER_ID'].nunique())
print("Accounts:", df_account['CUSTOMER_ID'].nunique())
print("Loans:", df_loan['CUSTOMER_ID'].nunique())

print("Customer rows:", len(df_customer))
print("Account rows:", len(df_account))
print("Loan rows:", len(df_loan))

# Keep one record per customer ID
df_customer = df_customer.drop_duplicates(
    subset=['CUSTOMER_ID'],
    keep='first'
)

print("Unique customers:", len(df_customer))

check = pd.read_csv("../data/clean/clean_customers_mysql.csv")
print("CSV rows:", len(check))
print("Unique IDs:", check['customer_id'].nunique())

# Keep one record per customer
df_customer = df_customer.drop_duplicates(
    subset=['CUSTOMER_ID'],
    keep='first'
)

print("Customer rows:", len(df_customer))
print("Unique IDs:", df_customer['CUSTOMER_ID'].nunique())

# Prepare customer data for MySQL
df_customer_mysql = df_customer[
    ['CUSTOMER_ID', 'FULL_NAME', 'City', 'Occupation',
     'DOB', 'AGE', 'AGE_GROUP']
].copy()

df_customer_mysql.columns = [
    'customer_id', 'full_name', 'city', 'occupation',
    'dob', 'age', 'age_group'
]

df_customer_mysql.to_csv(
    "../data/clean/clean_customers_mysql.csv",
    index=False
)

check = pd.read_csv("../data/clean/clean_customers_mysql.csv")

print("CSV rows:", len(check))
print("Unique IDs:", check['customer_id'].nunique())

# Prepare account data for MySQL
df_account_mysql = df_account[
    ['ACCOUNT_ID', 'CUSTOMER_ID', 'BRANCH_ID', 'OPENING_BALANCE',
     'ACCOUNT_OPEN_DATE', 'OPEN_YEAR', 'OPEN_MONTH', 'ACCOUNT_TYPE',
     'ACCOUNT_STATUS', 'IS_CASA']
].copy()

df_account_mysql.columns = [
    'account_id', 'customer_id', 'branch_id', 'opening_balance',
    'account_open_date', 'open_year', 'open_month', 'account_type',
    'account_status', 'is_casa'
]

df_account_mysql.to_csv(
    "../data/clean/clean_accounts_mysql.csv",
    index=False
)

print("Rows:", len(df_account_mysql))
print("Unique accounts:", df_account_mysql['account_id'].nunique())

check = pd.read_csv("../data/clean/clean_accounts_mysql.csv")

print(check.shape)
print(check.columns.tolist())
print("Unique account IDs:", check['account_id'].nunique())

# Check account duplicates
duplicates = df_account[
    df_account.duplicated('ACCOUNT_ID', keep=False)
]

print(duplicates[['ACCOUNT_ID', 'CUSTOMER_ID', 'BRANCH_ID']].head(10))

# Inspect one duplicated account
print(df_account[df_account['ACCOUNT_ID'] == 'A00001'])

# Keep one record per account
df_account = df_account.drop_duplicates(
    subset=['ACCOUNT_ID'],
    keep='first'
)

print("Account rows:", len(df_account))
print("Unique accounts:", df_account['ACCOUNT_ID'].nunique())

# Prepare account data for MySQL
df_account_mysql = df_account[
    ['ACCOUNT_ID', 'CUSTOMER_ID', 'BRANCH_ID', 'OPENING_BALANCE',
     'ACCOUNT_OPEN_DATE', 'OPEN_YEAR', 'OPEN_MONTH', 'ACCOUNT_TYPE',
     'ACCOUNT_STATUS', 'IS_CASA']
].copy()

df_account_mysql.columns = [
    'account_id', 'customer_id', 'branch_id', 'opening_balance',
    'account_open_date', 'open_year', 'open_month', 'account_type',
    'account_status', 'is_casa'
]

df_account_mysql.to_csv(
    "../data/clean/clean_accounts_mysql.csv",
    index=False
)

check = pd.read_csv("../data/clean/clean_accounts_mysql.csv")

print("CSV rows:", len(check))
print("Unique IDs:", check['account_id'].nunique())

# Prepare transaction data for MySQL
df_transaction_mysql = df_transaction[
    ['TRANSACTION_ID', 'ACCOUNT_ID', 'TRANSACTION_DATE',
     'YEAR', 'MONTH', 'QUARTER', 'YEAR_MONTH',
     'TRANSACTION_MEDIA', 'TRANSACTION_TYPE',
     'TRANSACTION_AMOUNT', 'IS_INFLOW']
].copy()

df_transaction_mysql.columns = [
    'transaction_id', 'account_id', 'transaction_date',
    'year', 'month', 'quarter', 'year_month',
    'transaction_media', 'transaction_type',
    'transaction_amount', 'is_inflow'
]

df_transaction_mysql.to_csv(
    "../data/clean/clean_transactions_mysql.csv",
    index=False
)

print("Rows:", len(df_transaction_mysql))
print("Unique transactions:", df_transaction_mysql['transaction_id'].nunique())

# Find duplicated transaction IDs
duplicates = df_transaction[
    df_transaction.duplicated('TRANSACTION_ID', keep=False)
]

print(duplicates[['TRANSACTION_ID', 'ACCOUNT_ID',
                  'TRANSACTION_DATE', 'TRANSACTION_TYPE',
                  'TRANSACTION_AMOUNT']].head(10))

# Inspect one duplicate
print(
    df_transaction[
        df_transaction['TRANSACTION_ID'] == 'T00001'
    ]
)

# Create unique transaction IDs
df_transaction['TRANSACTION_ID'] = [
    f"T{i:05d}" for i in range(1, len(df_transaction) + 1)
]

print("Rows:", len(df_transaction))
print("Unique transactions:", df_transaction['TRANSACTION_ID'].nunique())

# Prepare transaction data for MySQL
df_transaction_mysql = df_transaction[
    ['TRANSACTION_ID', 'ACCOUNT_ID', 'TRANSACTION_DATE',
     'YEAR', 'MONTH', 'QUARTER', 'YEAR_MONTH',
     'TRANSACTION_MEDIA', 'TRANSACTION_TYPE',
     'TRANSACTION_AMOUNT', 'IS_INFLOW']
].copy()

df_transaction_mysql.columns = [
    'transaction_id', 'account_id', 'transaction_date',
    'year', 'month', 'quarter', 'year_month',
    'transaction_media', 'transaction_type',
    'transaction_amount', 'is_inflow'
]

df_transaction_mysql.to_csv(
    "../data/clean/clean_transactions_mysql.csv",
    index=False
)

check = pd.read_csv("../data/clean/clean_transactions_mysql.csv")

print("CSV rows:", len(check))
print("Unique IDs:", check['transaction_id'].nunique())

# Check loan IDs
print("Loan rows:", len(df_loan))
print("Unique loans:", df_loan['LOAN_ID'].nunique())

# Inspect duplicated loan IDs
duplicates = df_loan[
    df_loan.duplicated('LOAN_ID', keep=False)
]

print(duplicates.head(10))

# Inspect one duplicate loan
print(
    df_loan[
        df_loan['LOAN_ID'] == 'L00001'
    ]
)

# Create unique loan IDs
df_loan['LOAN_ID'] = [
    f"L{i:05d}" for i in range(1, len(df_loan) + 1)
]

print("Loan rows:", len(df_loan))
print("Unique loans:", df_loan['LOAN_ID'].nunique())

# Prepare loan data for MySQL
df_loan_mysql = df_loan[
    ['LOAN_ID', 'CUSTOMER_ID', 'BRANCH_ID', 'LOAN_AMOUNT']
].copy()

df_loan_mysql.columns = [
    'loan_id', 'customer_id', 'branch_id', 'loan_amount'
]

df_loan_mysql.to_csv(
    "../data/clean/clean_loans_mysql.csv",
    index=False
)

check = pd.read_csv("../data/clean/clean_loans_mysql.csv")

print("CSV rows:", len(check))
print("Unique IDs:", check['loan_id'].nunique())