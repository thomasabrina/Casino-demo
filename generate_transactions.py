import csv
import random
from datetime import datetime, timedelta

# Define the headers for the CSV
headers = [
    "Transaction ID", "User ID", "Amount", "Date", "Type", 
    "Game ID", "Currency", "Status", "Payment Method", "Notes"
]

# Define some sample data to use in the transactions
transaction_types = ["Deposit", "Withdrawal", "Bet", "Win"]
currencies = ["USD", "EUR", "GBP", "JPY"]
statuses = ["Pending", "Completed", "Failed"]
payment_methods = ["Credit Card", "Bank Transfer", "PayPal", "Crypto"]
notes = ["First", "Second", "Third", "Fourth", "Fifth"]

# Function to generate a random date
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Get the number of transactions from user input
num_transactions = int(input("Enter the number of transactions to generate: "))

transactions = []
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

for i in range(num_transactions):
    transaction = [
        i + 1001,  # Transaction ID
        random.randint(500, 1000),  # User ID
        random.randint(100, 100000),  # Amount
        random_date(start_date, end_date).strftime("%m/%d/%Y"),  # Date
        random.choice(transaction_types),  # Type
        random.randint(100, 200),  # Game ID
        random.choice(currencies),  # Currency
        random.choice(statuses),  # Status
        random.choice(payment_methods),  # Payment Method
        random.choice(notes)  # Notes
    ]
    transactions.append(transaction)

# Write to CSV
with open('transaction_template.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(transactions)

print(f"transaction_template.csv has been created with {num_transactions} transactions.")
