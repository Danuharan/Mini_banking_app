import os

def get_customer_info():
    name = input("Enter your Name: ")
    address = input("Enter your Address: ")
    username = input("Enter your User Name: ")
    password = input("Enter your Password: ")
    return [name, address, username, password]

def create_customer_next_id():
    if not os.path.exists("customers.txt") or os.stat("customers.txt").st_size == 0:
        return "U001"
    with open("customers.txt", "r") as customer_file:
        last_line = customer_file.readlines()[-1]
        last_id = last_line.split(",")[0]
        return f"U{int(last_id[1:]) + 1:03}"

def create_customer_and_user():
    customers = get_customer_info()
    user_id = create_customer_next_id()
    with open("customers.txt", "a") as customer_file, open("users.txt", "a") as user_file:
        customer_file.write(f"{user_id},{customers[0]},{customers[1]}\n")
        user_file.write(f"{customers[2]},{customers[3]},0.0\n")  # initial balance
    print(f"\n Customer created successfully with ID: {user_id}")

def view_all_customers():
    if not os.path.exists("customers.txt"):
        print(" No customer records found.")
        return
    print("\n--- Customer List ---")
    with open("customers.txt", "r") as customer_file:
        for customer in customer_file.readlines():
            print(customer.strip())

def user_login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if not os.path.exists("users.txt"):
        print(" No users found.")
        return None
    with open("users.txt", "r") as user_file:
        for line in user_file:
            u, p, balance = line.strip().split(",")
            if u == username and p == password:
                print(f" Welcome, {username}!")
                return username
    print(" Invalid credentials.")
    return None

def load_users():
    users = {}
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                username, password, balance = line.strip().split(",")
                users[username] = {"password": password, "balance": float(balance)}
    return users

def save_users(users):
    with open("users.txt", "w") as f:
        for username in users:
            password = users[username]["password"]
            balance = users[username]["balance"]
            f.write(f"{username},{password},{balance}\n")

def deposit(users, username):
    amount = float(input("Enter amount to deposit: "))
    users[username]["balance"] += amount
    save_users(users)
    print(f" Deposited ₹{amount:.2f}. New balance: ₹{users[username]['balance']:.2f}")

def withdraw(users, username):
    amount = float(input("Enter amount to withdraw: "))
    if amount <= users[username]["balance"]:
        users[username]["balance"] -= amount
        save_users(users)
        print(f" Withdrew ₹{amount:.2f}. New balance: ₹{users[username]['balance']:.2f}")
    else:
        print(" Insufficient balance.")

def check_balance(users, username):
    print(f" Current balance: ₹{users[username]['balance']:.2f}")

def user_menu(users, username):
    while True:
        print("\n--- User Menu ---")
        print("1. Deposit\n2. Withdraw\n3. Check Balance\n4. Logout")
        choice = input("Enter your choice: ")
        if choice == "1":
            deposit(users, username)
        elif choice == "2":
            withdraw(users, username)
        elif choice == "3":
            check_balance(users, username)
        elif choice == "4":
            print(" Logged out.")
            break
        else:
            print(" Invalid choice.")

def main():
    while True:
        print("\n===== Mini Bank App =====")
        print("1. Create Customer")
        print("2. View All Customers")
        print("3. User Login")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_customer_and_user()
        elif choice == "2":
            view_all_customers()
        elif choice == "3":
            username = user_login()
            if username:
                users = load_users()
                user_menu(users, username)
        elif choice == "4":
            print("👋 Exiting...")
            break
        else:
            print(" Invalid input. Try again.")

if __name__ == "__main__":
    main()