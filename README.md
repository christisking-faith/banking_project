# Banking System – Mini Project

A menu-driven, Python-based banking simulation. Create an account, log in securely with a PIN, and perform everyday banking operations from the terminal.

## Features

- Create an account (name, phone number, 4-digit PIN with confirmation)
- Login with account number + PIN (3 attempts)
- Check balance
- Deposit / Withdraw (with balance checks)
- Transfer money between accounts (PIN-confirmed)
- Transaction history with date & time
- Change PIN (old PIN → new PIN → confirm)
- Logout and return to main menu
- Data is saved to `bank_data.json`, so accounts survive restarts

## Python Concepts Used

Variables & data types · Conditional statements · Loops · Functions · Lists & dictionaries · String operations · Modules (`random`, `datetime`, plus `json` / `os` for saving)

## How to Run

Requires Python 3.8+. No external packages.

```bash
python main.py
```

## Flow

```
CREATE ACCOUNT → Account Number + PIN → LOGIN → ACCOUNT MENU → LOGOUT → MAIN MENU
```

## Project Structure

```
banking-system/
├── main.py        # the whole application
├── README.md
└── .gitignore     # keeps saved account data out of the repo
```
