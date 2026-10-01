"""
Banking System - Mini Project
A menu-driven banking simulation using core Python concepts:
variables, conditionals, loops, functions, lists & dicts, string ops, modules.
"""

import json
import os
import random
from datetime import datetime

DATA_FILE = "bank_data.json"
MAX_LOGIN_ATTEMPTS = 3

# accounts = { "1234567890": {"name", "phone", "pin", "balance", "transactions": [..]} }
accounts = {}


# ---------------------------------------------------------------- storage
def load_accounts():
    """Load saved accounts from disk (if any)."""
    global accounts
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                accounts = json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Warning: could not read saved data. Starting fresh.")
            accounts = {}


def save_accounts():
    """Save all accounts to disk so data survives restarts."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(accounts, f, indent=4)
    except OSError:
        print("Warning: could not save data.")


# ---------------------------------------------------------------- helpers
def now():
    """Current date and time as a readable string."""
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def generate_account_number():
    """Generate a unique 10-digit account number using random."""
    while True:
        acc_no = str(random.randint(10**9, 10**10 - 1))
        if acc_no not in accounts:
            return acc_no


def add_transaction(acc_no, kind, amount, details=""):
    """Record a transaction with date & time on an account."""
    accounts[acc_no]["transactions"].append({
        "time": now(),
        "type": kind,
        "amount": amount,
        "details": details,
        "balance": accounts[acc_no]["balance"],
    })


def get_amount(prompt):
    """Ask for a positive number. Returns None if invalid."""
    value = input(prompt).strip()
    try:
        amount = round(float(value), 2)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return None
    if amount <= 0:
        print("Amount must be greater than zero.")
        return None
    return amount


def get_pin(prompt):
    """Ask for a 4-digit PIN. Returns None if invalid."""
    pin = input(prompt).strip()
    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be exactly 4 digits.")
        return None
    return pin


# ---------------------------------------------------------------- main menu actions
def create_account():
    print("\n--- CREATE ACCOUNT ---")

    name = input("Enter your name: ").strip()
    if not name or not name.replace(" ", "").isalpha():
        print("Name must contain only letters and spaces.")
        return

    phone = input("Enter phone number (10 digits): ").strip()
    if len(phone) != 10 or not phone.isdigit():
        print("Phone number must be exactly 10 digits.")
        return

    pin = get_pin("Create a 4-digit PIN: ")
    if pin is None:
        return
    if input("Confirm PIN: ").strip() != pin:
        print("PINs do not match. Account not created.")
        return

    acc_no = generate_account_number()
    accounts[acc_no] = {
        "name": name.title(),
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": [],
    }
    add_transaction(acc_no, "ACCOUNT OPENED", 0.0, "Account created")
    save_accounts()

    print("\nAccount created successfully!")
    print(f"Account Holder : {accounts[acc_no]['name']}")
    print(f"Account Number : {acc_no}   <-- remember this!")


def login():
    """Returns the account number on success, otherwise None."""
    print("\n--- LOGIN ---")
    acc_no = input("Enter account number: ").strip()
    if acc_no not in accounts:
        print("Account not found.")
        return None

    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        pin = input("Enter PIN: ").strip()
        if pin == accounts[acc_no]["pin"]:
            print(f"\nWelcome, {accounts[acc_no]['name']}!")
            return acc_no
        remaining = MAX_LOGIN_ATTEMPTS - attempt
        if remaining:
            print(f"Incorrect PIN. {remaining} attempt(s) left.")
    print("Too many failed attempts. Returning to main menu.")
    return None


# ---------------------------------------------------------------- account menu actions
def check_balance(acc_no):
    print(f"\nCurrent balance: Rs. {accounts[acc_no]['balance']:.2f}")


def deposit(acc_no):
    amount = get_amount("\nEnter amount to deposit: Rs. ")
    if amount is None:
        return
    accounts[acc_no]["balance"] += amount
    add_transaction(acc_no, "DEPOSIT", amount)
    save_accounts()
    print(f"Rs. {amount:.2f} deposited. New balance: Rs. {accounts[acc_no]['balance']:.2f}")


def withdraw(acc_no):
    amount = get_amount("\nEnter amount to withdraw: Rs. ")
    if amount is None:
        return
    if amount > accounts[acc_no]["balance"]:
        print("Insufficient balance.")
        return
    accounts[acc_no]["balance"] -= amount
    add_transaction(acc_no, "WITHDRAW", amount)
    save_accounts()
    print(f"Rs. {amount:.2f} withdrawn. New balance: Rs. {accounts[acc_no]['balance']:.2f}")


def transfer(acc_no):
    receiver = input("\nEnter receiver account number: ").strip()
    if receiver not in accounts:
        print("Receiver account not found.")
        return
    if receiver == acc_no:
        print("You cannot transfer money to your own account.")
        return

    amount = get_amount("Enter amount to transfer: Rs. ")
    if amount is None:
        return
    if amount > accounts[acc_no]["balance"]:
        print("Insufficient balance.")
        return

    if input("Enter your PIN to confirm: ").strip() != accounts[acc_no]["pin"]:
        print("Incorrect PIN. Transfer cancelled.")
        return

    accounts[acc_no]["balance"] -= amount
    accounts[receiver]["balance"] += amount
    add_transaction(acc_no, "TRANSFER OUT", amount, f"To {receiver} ({accounts[receiver]['name']})")
    add_transaction(receiver, "TRANSFER IN", amount, f"From {acc_no} ({accounts[acc_no]['name']})")
    save_accounts()
    print(f"Rs. {amount:.2f} transferred to {accounts[receiver]['name']}.")
    print(f"New balance: Rs. {accounts[acc_no]['balance']:.2f}")


def transaction_history(acc_no):
    history = accounts[acc_no]["transactions"]
    print("\n--- TRANSACTION HISTORY ---")
    if not history:
        print("No transactions yet.")
        return
    print(f"{'Date & Time':<21}{'Type':<16}{'Amount':>12}{'Balance':>12}  Details")
    print("-" * 80)
    for t in history:
        print(f"{t['time']:<21}{t['type']:<16}{t['amount']:>12.2f}{t['balance']:>12.2f}  {t['details']}")


def change_pin(acc_no):
    if input("\nEnter old PIN: ").strip() != accounts[acc_no]["pin"]:
        print("Incorrect old PIN.")
        return
    new_pin = get_pin("Enter new PIN: ")
    if new_pin is None:
        return
    if new_pin == accounts[acc_no]["pin"]:
        print("New PIN must be different from the old PIN.")
        return
    if input("Confirm new PIN: ").strip() != new_pin:
        print("PINs do not match. PIN not changed.")
        return
    accounts[acc_no]["pin"] = new_pin
    add_transaction(acc_no, "PIN CHANGED", 0.0, "PIN updated")
    save_accounts()
    print("PIN changed successfully.")


# ---------------------------------------------------------------- menus
def account_menu(acc_no):
    while True:
        print("\n+---------------------------+")
        print("|        ACCOUNT MENU       |")
        print("+---------------------------+")
        print("| 1. Check Balance          |")
        print("| 2. Deposit                |")
        print("| 3. Withdraw               |")
        print("| 4. Transfer               |")
        print("| 5. Transaction History    |")
        print("| 6. Change PIN             |")
        print("| 7. Logout                 |")
        print("+---------------------------+")
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            check_balance(acc_no)
        elif choice == "2":
            deposit(acc_no)
        elif choice == "3":
            withdraw(acc_no)
        elif choice == "4":
            transfer(acc_no)
        elif choice == "5":
            transaction_history(acc_no)
        elif choice == "6":
            change_pin(acc_no)
        elif choice == "7":
            print("\nLogged out successfully.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


def main():
    load_accounts()
    print("=" * 35)
    print("   WELCOME TO PYTHON BANK")
    print("=" * 35)

    while True:
        print("\n--- MAIN MENU ---")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            acc_no = login()
            if acc_no:
                account_menu(acc_no)
        elif choice == "3":
            print("\nThank you for banking with us. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
