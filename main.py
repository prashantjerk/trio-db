import pymysql
import pymysql.cursors
from datetime import datetime

def connect_to_database():
    try:
        cnx = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='Opurchase'
        )
        return cnx
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def login(cnx):
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    print("----------- Customer Interface -----------")
    print("----------- Login Now -----------")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    try:
        login_query = """
        SELECT customer_Id, fName, lName, DOB, street, zipCode, city, country 
        FROM Customer 
        WHERE username = %s AND password = %s
        """
        cursor.execute(login_query, (username, password))
        result = cursor.fetchone()

        if result:
            print(f"\nLogin successful! Welcome, {result['fName']} {result['lName']}!")
            print("\nYour Profile:")
            print(f"Address: {result['street']}")
            print(f"City: {result['city']}, {result['country']}")
            print(f"Zip Code: {result['zipCode']}")

                    #ask the logged in user if they want to start the purchase or see the history
            print("Type 1 if you want to buy some items.")
            print("Type 2 if you want to see the bill history.")
        
            while True:
                request = input("Type here: ")
                if not request:
                    print("Input cannot be empty.")
                    continue
                elif request == '1':
                    purchase(cnx, result['customer_Id'])
                    return None
                elif request == '2':
                    recent_bills(cnx, result['customer_Id'])
                    return None
                else:
                    print("Invalid input. The input should be either '1' or '2'")
        else:
            print("Invalid credentials. Please check your username and password.")
        
    except pymysql.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()

def purchase(cnx, customer_id):
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    print("\n---- Purchase Items ----")
    cart = []

    try:
        # Start a transaction
        cnx.begin()

        while True:
            item_name = input("Enter the name of the item you want to buy (or type 'done' to finish): ").strip()
            if item_name.lower() == 'done':
                break

            quantity = input(f"Enter the quantity for '{item_name}': ").strip()
            if not quantity.isdigit() or int(quantity) <= 0:
                print("Invalid quantity. Please enter a positive number.")
                continue

            # Check if the item is available in stock
            check_item_query = "SELECT item_Id, price, quantity FROM Item WHERE name = %s"
            cursor.execute(check_item_query, (item_name,))
            item = cursor.fetchone()

            if not item:
                print(f"'{item_name}' is not available in stock.")
            elif int(quantity) > item['quantity']:
                print(f"Only {item['quantity']} units of '{item_name}' are available.")
            else:
                # Add the item to the cart
                cart.append((item['item_Id'], item_name, int(quantity), item['price']))
                print(f"Added {quantity} units of '{item_name}' to your cart.")

        # If the cart is empty, exit
        if not cart:
            print("Your cart is empty. No items purchased.")
            cnx.rollback()
            return

        # Calculate the total amount
        total_amount = sum(item[2] * item[3] for item in cart)
        print(f"\nYour total amount is: ${total_amount:.2f}")

        # Check user's balance
        balance_query = "SELECT balance FROM BankInfo WHERE customer_Id = %s"
        cursor.execute(balance_query, (customer_id,))
        balance_result = cursor.fetchone()

        if balance_result and balance_result['balance'] >= total_amount:
            # Deduct the total amount from the user's balance
            update_balance_query = "UPDATE BankInfo SET balance = balance - %s WHERE customer_Id = %s"
            cursor.execute(update_balance_query, (total_amount, customer_id))

            # Insert the transaction into the Bill table
            insert_bill_query = "INSERT INTO Bill (customer_Id, totalAmount) VALUES (%s, %s)"
            cursor.execute(insert_bill_query, (customer_id, total_amount))
            bill_id = cursor.lastrowid

            # Insert each item into the BillItems table
            for item_id, item_name, qty, price in cart:
                insert_bill_item_query = """
                    INSERT INTO BillItems (bill_Id, item_Id, quantity, priceAfterDiscount)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_bill_item_query, (bill_id, item_id, qty, price * qty))

            # Update the stock for the purchased items
            for item_id, item_name, qty, price in cart:
                update_stock_query = "UPDATE Item SET quantity = quantity - %s WHERE item_Id = %s"
                cursor.execute(update_stock_query, (qty, item_id))

            # Commit the transaction
            cnx.commit()
            print("\nPurchase successful! Thank you for shopping.")
        else:
            print("\nInsufficient balance. Please add more funds to your account.")
            cnx.rollback()
    except pymysql.Error as e:
        # Rollback the transaction in case of any error
        cnx.rollback()
        print(f"Database error: {e}")
    finally:
        cursor.close()

def recent_bills(cnx, customer_id):
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    print("\n----------- Recent Bills -----------")

    try:
        # Query to fetch the last 5 bills of the customer
        bills_query = """
        SELECT bill_id, totalAmount
        FROM Bill
        WHERE customer_Id = %s
        ORDER BY bill_Id
        LIMIT 5
        """
        cursor.execute(bills_query, (customer_id,))
        bills = cursor.fetchall()

        if bills:
            print("\nYour last 5 bills:")
            for bill in bills:
                print(f"Bill ID: {bill['bill_id']}, Total Amount: ${bill['totalAmount']}")
        else:
            print("\nNo bill history found. No purchase made yet.")
    except pymysql.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()


def input_for_registration(cursor):
    # First name validation
    while True:
        fname = input("First Name: ").strip()
        if not fname:
            print("First name cannot be empty.")
            continue
        break

    # Last name validation
    while True:
        lname = input("Last Name: ").strip()
        if not lname:
            print("Last name cannot be empty.")
            continue
        break

    # Date of birth validation
    while True:
        try:
            year = input("Year of birth (e.g., 1990): ").strip()
            month = input("Month of birth (e.g., 01 for January): ").strip().zfill(2)
            date = input("Date of birth (e.g., 31): ").strip().zfill(2)

            # Construct and validate the date
            dob = f"{year}-{month}-{date}"
            datetime.strptime(dob, "%Y-%m-%d")  # Raise ValueError if invalid

            if not (1900 <= int(year) <= datetime.now().year):
                print("Please enter a valid year between 1900 and the present.")
                continue
            break
        except ValueError:
            print("Invalid date. Please enter a valid date.")

    # Address validation
    street = input("Street (e.g., 1501 Lakeside Dr): ").strip()

    # Zipcode validation
    while True:
        zipcode = input("Zipcode (e.g., 24501): ").strip()
        if len(zipcode) == 5 and zipcode.isdigit():
            break
        print("Please enter a valid 5-digit zipcode.")
    
    #city information
    while True:
        city = input("City: ")
        if not city:
            print("City cannot be empty")
            continue
        break

    # Country information
    while True:
        country = input("Country: ").strip()
        if not country:
            print("Country cannot be empty.")
            continue
        break

    # Username validation
    while True:
        username = input("Username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue

        try:
            fetch_query = "SELECT customer_Id FROM customer WHERE username = %s"
            cursor.execute(fetch_query, (username,))
            result = cursor.fetchone()

            if result:
                print("Username already exists. Please choose another.")
            else:
                break
        except pymysql.Error as e:
            print(f"Database error: {e}")
            return None

    # Password validation
    while True:
        password = input("Password: ").strip()
        if len(password) < 6:
            print("Password too short. Must be at least 6 characters.")
            continue
        break

    # Return collected data
    return {
        "fname": fname,
        "lname": lname,
        "dob": dob,
        "street": street,
        "zipcode": zipcode,
        "city": city,
        "country": country,
        "username": username,
        "password": password,
    }


def register(cnx):
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    print("---------- Welcome to our store ---------")
    print("--------- Better late than never ---------")

    try:
        # Collect registration data
        user_data = input_for_registration(cursor)

        if user_data:
            # Insert into database
            insert_query = """
                INSERT INTO customer (fname, lname, dob, street, zipcode, city, country, username, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                insert_query,
                (
                    user_data["fname"],
                    user_data["lname"],
                    user_data["dob"],
                    user_data["street"],
                    user_data["zipcode"],
                    user_data["city"],
                    user_data["country"],
                    user_data["username"],
                    user_data["password"],
                ),
            )
            cnx.commit()
            print("Registration successful! Welcome, {}!".format(user_data["fname"]))
    except pymysql.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()

   

def customer_interface(cnx):
    print("Are you a returning user? (yes/no)")
    user_input = input("Type here: ").lower()

    # ask users if they are new or returning
    if user_input == "yes":
        login(cnx)
    elif user_input == "no":
        register(cnx)
    else:
        print("Invalid Input")

import pymysql

def view_recent_bills(cnx):
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    try:
        print("\n--- Last 5 Bills ---")
        query = """
            SELECT Bill.bill_Id, Customer.fName, Customer.lName, Bill.totalAmount
            FROM Bill
            JOIN Customer ON Bill.customer_Id = Customer.customer_Id
            ORDER BY Bill.bill_Id DESC
            LIMIT 5;
        """
        cursor.execute(query)
        bills = cursor.fetchall()

        if bills:
            print("\n" + "-" * 50)
            print(f"{'Bill ID':<10} {'Customer Name':<30} {'Total Amount':>10}")
            print("-" * 50)
            for bill in bills:
                customer_name = f"{bill['fName']} {bill['lName']}"
                print(f"{bill['bill_Id']:<10} {customer_name:<30} ${bill['totalAmount']:>10.2f}")
            print("-" * 50)
        else:
            print("\nNo bills found.")
    except pymysql.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()


def view_average_purchases(cnx):
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    try:
        query = "SELECT AVG(totalAmount) AS average_purchase FROM Bill"
        cursor.execute(query)
        result = cursor.fetchone()

        if result and result['average_purchase']:
            print(f"\n---- Average Purchase ----")
            print(f"The average purchase amount is: ${result['average_purchase']:.2f}")
        else:
            print("No purchase data available.")
    except pymysql.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()

def manager_interface(cnx):
    """Main manager interface."""
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    print("----------- Manager Interface -----------")
    print("----------- Login Now -----------")

    create_manager = """
                INSERT INTO Manager () VALUES ()
                """
    
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    try:
        login_query = """
            SELECT managerId, username
            FROM Manager 
            WHERE username = %s AND password = %s
        """
        cursor.execute(login_query, (username, password))
        result = cursor.fetchone()

        if result:
            print(f"\nLogin successful! Welcome, {result['username']}!")
            while True:
                print("\nWhat would you like to do?")
                print("1: See the current bills (last 5 bills)")
                print("2: See the average purchases")
                print("3: Logout")

                choice = input("Enter your choice: ").strip()
                if choice == "1":
                    view_last_5_bills(cnx)
                elif choice == "2":
                    view_average_purchases(cnx)
                elif choice == "3":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please select a valid option.")
        else:
            print("Invalid manager credentials.")
    except pymysql.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()


def main():
    cnx = connect_to_database()
    if not cnx:
        return

    try:
        while True:
            print("\nAre you a Customer or Manager?")
            print("1. Customer (C)")
            print("2. Manager (M)")
            print("3. Exit (E)")
            
            user_type = input("Type here (C/M/E): ").upper()

            if user_type == "C":
                customer_interface(cnx)
                break
            elif user_type == "M":
                manager_interface(cnx)
                break
            elif user_type == "E":
                print("Thank you for using our system. Goodbye!")
                break
            else:
                print("Invalid user type. Please try again.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cnx.close()

if __name__ == "__main__":
    main()