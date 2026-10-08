from account_operations import (
    create_account,
    view_accounts,
    search_account,
    deposit_money,
    withdraw_money,
    check_balance,
    transaction_history,
    update_account,
    delete_account
)

def menu():
    while True:
        print("\n")
        print("=" * 45)
        print("       BANK MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. Create Account")
        print("2. View All Accounts")
        print("3. Search Account")
        print("4. Deposit Money")
        print("5. Withdraw Money")
        print("6. Check Balance")
        print("7. Transaction History")
        print("8. Update Account")
        print("9. Delete Account")
        print("10. Exit")
        print("=" * 45)

        choice = input("Enter Your Choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            view_accounts()
        elif choice == "3":
            search_account()
        elif choice == "4":
            deposit_money()
        elif choice == "5":
            withdraw_money()
        elif choice == "6":
            check_balance()
        elif choice == "7":
            transaction_history()
        elif choice == "8":
            update_account()
        elif choice == "9":
            delete_account()
        elif choice == "10":
            print("\nThank you for using Bank Management System!")
            break
        else:
            print("Invalid choice. Please try again.")