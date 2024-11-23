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
            return result
        else:
            print("Invalid credentials. Please check your username and password.")
            return None

    except pymysql.Error as e:
        print(f"Database error: {e}")
        return None
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

    if user_input == "yes":
        return login(cnx)
    elif user_input == "no":
        register(cnx)
        return None
    else:
        print("Invalid Input")
        return None


def manager_interface(cnx):
    cursor = cnx.cursor(pymysql.cursors.DictCursor)
    print("----------- Manager Interface -----------")
    print("----------- Login Now -----------")
    
    create_manager = """
                INSERT INTO Manager () VALUES ()
                """
    
    cursor.execute(create_manager)
    
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
            return result
        else:
            print("Invalid manager credentials.")
            return None

    except pymysql.Error as e:
        print(f"Database error: {e}")
        return None
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
                result = customer_interface(cnx)
                if result:
                    # Add customer menu options here
                    break
            elif user_type == "M":
                result = manager_interface(cnx)
                if result:
                    # Add manager menu options here
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