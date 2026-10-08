from db_config import connect


# ==========================================
# 1. CREATE ACCOUNT
# ==========================================

def create_account():
    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    phone = input("Enter Phone: ")
    address = input("Enter Address: ")

    try:
        initial_balance = float(input("Enter Initial Balance: "))
    except ValueError:
        print("Please enter a valid amount.")
        return

    if initial_balance < 0:
        print("Initial balance cannot be negative.")
        return

    db = connect()

    if db is None:
        return

    cursor = db.cursor()

    try:
        sql = """
        INSERT INTO accounts
        (name, email, phone, address, balance)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            name,
            email,
            phone,
            address,
            initial_balance
        )

        cursor.execute(sql, values)

        account_id = cursor.lastrowid

        # Save initial deposit in transaction history
        if initial_balance > 0:

            transaction_sql = """
            INSERT INTO transactions
            (account_id, transaction_type, amount)
            VALUES (%s, %s, %s)
            """

            cursor.execute(
                transaction_sql,
                (account_id, "DEPOSIT", initial_balance)
            )

        db.commit()

        print("\nAccount Created Successfully!")
        print("Your Account ID:", account_id)

    except Exception as error:
        db.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        db.close()


# ==========================================
# 2. VIEW ALL ACCOUNTS
# ==========================================

def view_accounts():
    print("\n========== ALL ACCOUNTS ==========")

    db = connect()

    if db is None:
        return

    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT id, name, email, phone, balance
            FROM accounts
            ORDER BY id
        """)

        accounts = cursor.fetchall()

        if not accounts:
            print("No accounts found.")
            return

        for account in accounts:
            print(
                f"ID: {account[0]} | "
                f"Name: {account[1]} | "
                f"Email: {account[2]} | "
                f"Phone: {account[3]} | "
                f"Balance: ₹{account[4]:.2f}"
            )

    except Exception as error:
        print("Error:", error)

    finally:
        cursor.close()
        db.close()


# ==========================================
# 3. SEARCH ACCOUNT
# ==========================================

def search_account():
    print("\n========== SEARCH ACCOUNT ==========")

    try:
        account_id = int(input("Enter Account ID: "))
    except ValueError:
        print("Invalid Account ID.")
        return

    db = connect()

    if db is None:
        return

    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT id, name, email, phone, address, balance
            FROM accounts
            WHERE id = %s
        """, (account_id,))

        account = cursor.fetchone()

        if account:
            print("\nAccount Found!")
            print("Account ID :", account[0])
            print("Name       :", account[1])
            print("Email      :", account[2])
            print("Phone      :", account[3])
            print("Address    :", account[4])
            print("Balance    :", f"₹{account[5]:.2f}")

        else:
            print("Account not found.")

    except Exception as error:
        print("Error:", error)

    finally:
        cursor.close()
        db.close()


# ==========================================
# 4. DEPOSIT MONEY
# ==========================================

def deposit_money():
    print("\n========== DEPOSIT MONEY ==========")

    try:
        account_id = int(input("Enter Account ID: "))
        amount = float(input("Enter Deposit Amount: "))
    except ValueError:
        print("Please enter valid values.")
        return

    if amount <= 0:
        print("Deposit amount must be greater than 0.")
        return

    db = connect()

    if db is None:
        return

    cursor = db.cursor()

    try:
        # Check account
        cursor.execute(
            "SELECT id FROM accounts WHERE id = %s",
            (account_id,)
        )

        account = cursor.fetchone()

        if account is None:
            print("Account not found.")
            return

        # Update balance
        cursor.execute("""
            UPDATE accounts
            SET balance = balance + %s
            WHERE id = %s
        """, (amount, account_id))

        # Save transaction
        cursor.execute("""
            INSERT INTO transactions
            (account_id, transaction_type, amount)
            VALUES (%s, %s, %s)
        """, (account_id, "DEPOSIT", amount))

        db.commit()

        print(f"₹{amount:.2f} deposited successfully!")

    except Exception as error:
        db.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        db.close()


# ==========================================
# 5. WITHDRAW MONEY
# ==========================================

def withdraw_money():
    print("\n========== WITHDRAW MONEY ==========")

    try:
        account_id = int(input("Enter Account ID: "))
        amount = float(input("Enter Withdrawal Amount: "))
    except ValueError:
        print("Please enter valid values.")
        return

    if amount <= 0:
        print("Withdrawal amount must be greater than 0.")
        return

    db = connect()

    if db is None:
        return

    cursor = db.cursor()

    try:
        # Get current balance
        cursor.execute("""
            SELECT balance
            FROM accounts
            WHERE id = %s
        """, (account_id,))

        account = cursor.fetchone()

        if account is None:
            print("Account not found.")
            return

        current_balance = float(account[0])

        # Check balance
        if current_balance < amount:
            print("Insufficient Balance!")
            print(
                f"Current Balance: ₹{current_balance:.2f}"
            )
            return

        # Update balance
        cursor.execute("""
            UPDATE accounts
            SET balance = balance - %s
            WHERE id = %s
        """, (amount, account_id))

        # Save transaction
        cursor.execute("""
            INSERT INTO transactions
            (account_id, transaction_type, amount)
            VALUES (%s, %s, %s)
        """, (account_id, "WITHDRAW", amount))

        db.commit()

        print(f"₹{amount:.2f} withdrawn successfully!")

    except Exception as error:
        db.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        db.close()


# ==========================================
# 6. CHECK BALANCE
# ==========================================

def check_balance():
    print("\n========== CHECK BALANCE ==========")

    try:
        account_id = int(input("Enter Account ID: "))
    except ValueError:
        print("Invalid Account ID.")
        return

    db = connect()

    if db is None:
        return

    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT name, balance
            FROM accounts
            WHERE id = %s
        """, (account_id,))

        account = cursor.fetchone()

        if account:
            print("\nAccount Holder:", account[0])
            print(
                "Current Balance:",
                f"₹{account[1]:.2f}"
            )

        else:
            print("Account not found.")

    except Exception as error:
        print("Error:", error)

    finally:
        cursor.close()
        db.close()


# ==========================================
# 7. TRANSACTION HISTORY
# ==========================================

def transaction_history():
    print("\n========== TRANSACTION HISTORY ==========")

    try:
        account_id = int(input("Enter Account ID: "))
    except ValueError:
        print("Invalid Account ID.")
        return

    db = connect()

    if db is None:
        return

    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT transaction_type,
                   amount,
                   transaction_date
            FROM transactions
            WHERE account_id = %s
            ORDER BY transaction_date DESC
        """, (account_id,))

        transactions = cursor.fetchall()

        if not transactions:
            print("No transactions found.")
            return

        for transaction in transactions:
            print(
                f"Type: {transaction[0]} | "
                f"Amount: ₹{transaction[1]:.2f} | "
                f"Date: {transaction[2]}"
            )

    except Exception as error:
        print("Error:", error)

    finally:
        cursor.close()
        db.close()


# ==========================================
# 8. UPDATE ACCOUNT
# ==========================================

def update_account():
    print("\n========== UPDATE ACCOUNT ==========")

    try:
        account_id = int(input("Enter Account ID: "))
    except ValueError:
        print("Invalid Account ID.")
        return

    name = input("Enter New Name: ")
    email = input("Enter New Email: ")
    phone = input("Enter New Phone: ")
    address = input("Enter New Address: ")

    db = connect()

    if db is None:
        return

    cursor = db.cursor()

    try:
        cursor.execute("""
            UPDATE accounts
            SET name = %s,
                email = %s,
                phone = %s,
                address = %s
            WHERE id = %s
        """, (
            name,
            email,
            phone,
            address,
            account_id
        ))

        if cursor.rowcount == 0:
            print("Account not found.")

        else:
            db.commit()
            print("Account updated successfully!")

    except Exception as error:
        db.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        db.close()


# ==========================================
# 9. DELETE ACCOUNT
# ==========================================

def delete_account():
    print("\n========== DELETE ACCOUNT ==========")

    try:
        account_id = int(input("Enter Account ID: "))
    except ValueError:
        print("Invalid Account ID.")
        return

    confirmation = input(
        "Are you sure you want to delete this account? (yes/no): "
    ).lower()

    if confirmation != "yes":
        print("Delete operation cancelled.")
        return

    db = connect()

    if db is None:
        return

    cursor = db.cursor()

    try:
        cursor.execute(
            "DELETE FROM accounts WHERE id = %s",
            (account_id,)
        )

        if cursor.rowcount == 0:
            print("Account not found.")

        else:
            db.commit()
            print("Account deleted successfully!")

    except Exception as error:
        db.rollback()
        print("Error:", error)

    finally:
        cursor.close()
        db.close()