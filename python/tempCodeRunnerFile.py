print("Rows after transaction merge:", len(txn_acc))
print(
    "B00021 transaction total:",
    txn_acc.loc[
        txn_acc['BRANCH_ID'] == 'B00021',
        'TRANSACTION_AMOUNT'
    ].sum()
)
