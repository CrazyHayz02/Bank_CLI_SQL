from db.user import create_user
from db.account import create_account, get_balance
from db.transactions import list_transactions
from services.banking_service import deposit, withdraw, transfer_money

def print_menu():
    print("\n=== Bank System Menu ===")
    print("1. Create user")
    print("2. Create account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Check balance")
    print("6. List transactions")
    print("7. Transfers")
    print("0. Exit\n")


def menu():
    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        try:
            if choice == "1":
                name = input("Enter name: ")
                email = input("Enter email: ")
                user_id = create_user(name, email)
                print(f"\nUser created with ID: {user_id}")

            elif choice == "2":
                user_id = int(input("Enter user ID: "))
                balance = float(input("Enter initial balance: "))
                account_id = create_account(user_id, balance)
                print(f"\nAccount created with ID: {account_id}")

            elif choice == "3":
                account_id = int(input("Enter account ID: "))
                amount = float(input("Enter deposit amount: "))
                new_balance = deposit(account_id, amount)
                print(f"\nNew balance: £{new_balance}")

            elif choice == "4":
                account_id = int(input("Enter account ID: "))
                amount = float(input("Enter withdraw amount: "))
                new_balance = withdraw(account_id, amount)
                print(f"\nNew balance: £{new_balance}")

            elif choice == "5":
                account_id = int(input("Enter account ID: "))
                balance = get_balance(account_id)
                print(f"\nCurrent balance: {balance}")
            
            elif choice == "6":
                account_id = int(input("Enter account ID: "))
                transactions = list_transactions(account_id)
                print("\nTransactions:")
                for tx in transactions:
                    print(tx)
            
            elif choice == "7":
                account_from = int(input("Enter account from: "))
                account_to = int(input("Enter account to: "))
                amount = float(input("Enter transfer amount: "))
                transfer_money(account_from, account_to, amount)
                print(f"\nTransfer was Successful")

            elif choice == "0":
                print("\nGoodbye!")
                break

            else:
                print("Invalid option. Try again.")

        except ValueError as ve:
            print("Input error:", ve)
        except Exception as e:
            print("Unexpected error:", e)


if __name__ == "__main__":
    menu()
