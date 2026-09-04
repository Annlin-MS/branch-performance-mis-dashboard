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

