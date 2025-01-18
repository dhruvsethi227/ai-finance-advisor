transactions = []

def add_transaction(transaction):
    transactions.append(transaction)

def get_transactions():
    return transactions

def update_transaction(index, updated_transaction):
    transactions[index] = updated_transaction

def delete_transaction(index):
    del transactions[index]