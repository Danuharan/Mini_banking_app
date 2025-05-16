import os

# File paths
USERS_FILE = "users.txt"
CUSTOMERS_FILE = "customers.txt"
ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"

# Global data
accounts = {}
current_user = None

# Load accounts from file
def load_accounts():
    data = {}
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                if not parts or len(parts) < 4:
                    continue
                acc_no, name, balance, txns = parts[0], parts[1], float(parts[2]), parts[3]
                transactions = txns.split("|") if txns else []
                data[acc_no] = {
                    "name": name,
                    "balance": balance,
                    "transactions": transactions
                }
    return data

# Save accounts to file
def save_accounts(data):
    with open(ACCOUNTS_FILE, "w") as f:
        for acc_no, details in data.items():
            txn_str = "|".join(details["transactions"])
            line = f"{acc_no};{details['name']};{details['balance']};{txn_str}\n"
            f.write(line)

# Generate customer ID
def generate_customer_id():
    if not os.path.exists(CUSTOMERS_FILE):
        return "C001"
    with open(CUSTOMERS_FILE, "r") as f:
        lines = f.readlines()
        if not lines:
            return "C001"
        last_id = lines[-1].split(";")[0]
        new_id = int(last_id[1:]) + 1
        return f"C{new_id:03d}"

# Generate account number
def generate_account_number():
    if not accounts:
        return "A001"
    last_acc = sorted(accounts.keys())[-1]
    new_number = int(last_acc[1:]) + 1
    return f"A{new_number:03d}"

# Save transaction
def record_transaction(account_number, detail):
    with open(TRANSACTIONS_FILE, "a") as f:
        f.write(f"{account_number}: {detail}\n")

# Admin register customer
def register_customer():
    name = input("Enter customer's full name: ")
    username = input("Choose a username: ")
    password = input("Choose a password: ")

    customer_id = generate_customer_id()
    with open(USERS_FILE, "a") as uf:
        uf.write(f"{username};{password};customer\n")
    with open(CUSTOMERS_FILE, "a") as cf:
        cf.write(f"{customer_id};{name}\n")

    print(f"Customer '{name}' registered successfully with ID: {customer_id}")

# Customer creates account
def create_account(username):
    account_number = generate_account_number()
    name = input("Enter your full name: ")
    while True:
        try:
            initial_balance = float(input("Enter initial deposit: "))
            if initial_balance < 0:
                print("Initial balance cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid amount.")

    accounts[account_number] = {
        "name": name,
        "balance": initial_balance,
        "transactions": [f"Account opened with {initial_balance}"]
    }

    save_accounts(accounts)
    record_transaction(account_number, f"Account created with initial balance: {initial_balance}")
    print(f"Account created! Your account number is {account_number}")

# Deposit
def deposit_money():
    acc_no = input("Enter account number: ")
    if acc_no not in accounts:
        print("Account not found.")
        return
    try:
        amount = float(input("Enter deposit amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        accounts[acc_no]["balance"] += amount
        detail = f"Deposit: +{amount}"
        accounts[acc_no]["transactions"].append(detail)
        record_transaction(acc_no, detail)
        save_accounts(accounts)
        print(f"Deposited. New balance: {accounts[acc_no]['balance']}")
    except ValueError:
        print("Invalid input.")

# Withdraw
def withdraw_money():
    acc_no = input("Enter account number: ")
    if acc_no not in accounts:
        print("Account not found.")
        return
    try:
        amount = float(input("Enter withdrawal amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        if accounts[acc_no]["balance"] < amount:
            print("Insufficient funds.")
            return
        accounts[acc_no]["balance"] -= amount
        detail = f"Withdrawal: -{amount}"
        accounts[acc_no]["transactions"].append(detail)
        record_transaction(acc_no, detail)
        save_accounts(accounts)
        print(f"Withdrawn. New balance: {accounts[acc_no]['balance']}")
    except ValueError:
        print("Invalid input.")

# Check balance
def check_balance():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        print(f"Current balance: {accounts[acc_no]['balance']}")
    else:
        print("Account not found.")

# View transactions
def transaction_history():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        print("Transactions:")
        for txn in accounts[acc_no]["transactions"]:
            print(txn)
    else:
        print("Account not found.")

# Admin menu
def admin_menu():
    while True:
        print("""
        --- Admin Menu ---
        1. Register New Customer
        2. Logout
        """)
        choice = input("Choice: ")
        if choice == "1":
            register_customer()
        elif choice == "2":
            print("Logging out...")
            break
        else:
            print("Invalid option.")

# Customer menu
def customer_menu(username):
    while True:
        print("""
        --- Customer Menu ---
        1. Create Account
        2. Deposit Money
        3. Withdraw Money
        4. Check Balance
        5. Transaction History
        6. Logout
        """)
        choice = input("Choice: ")
        if choice == "1":
            create_account(username)
        elif choice == "2":
            deposit_money()
        elif choice == "3":
            withdraw_money()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            transaction_history()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid option.")

# Login system
def login():
    username = input("Username: ")
    password = input("Password: ")

    if username == "admin" and password == "Hi123":
        print("Admin login successful.")
        admin_menu()
        return

    if not os.path.exists(USERS_FILE):
        print("No users found.")
        return

    with open(USERS_FILE, "r") as f:
        for line in f:
            user, pw, role = line.strip().split(";")
            if username == user and password == pw:
                print(f"{role.capitalize()} login successful.")
                customer_menu(username)
                return

    print("Invalid credentials.")

# Entry point
def main():
    global accounts
    accounts = load_accounts()
    while True:
        print("\n=== Welcome to Mini Banking App ===")
        login()

main()
