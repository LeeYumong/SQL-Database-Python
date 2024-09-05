import sqlite3

# Connect to the database or create it if it doesn't exist
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Create the table if it doesn't exist yet
def setup_database():
    schema = """
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.executescript(schema)
    conn.commit()

setup_database()

# Add a user to the database
def add_user(username, email):
    try:
        cursor.execute('''
        INSERT INTO User (username, email)
        VALUES (?, ?)
        ''', (username, email))
        conn.commit()
        print(f"Added user: {username}")
    except sqlite3.IntegrityError:
        print(f"Error! Either the username '{username}' or email '{email}' already exists.")

# Fetch and display all users
def list_users():
    cursor.execute('SELECT * FROM User')
    users = cursor.fetchall()
    if users:
        for user in users:
            print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Created At: {user[3]}")
    else:
        print("No users found in the database.")

# Remove a user by ID
def remove_user(user_id):
    cursor.execute('DELETE FROM User WHERE id = ?', (user_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print(f"User with ID {user_id} has been removed.")
    else:
        print(f"User with ID {user_id} not found.")

# Main function to interact with the user
def main():
    while True:
        print("\nWelcome to the User Management System!")
        print("1. Add a New User")
        print("2. List All Users")
        print("3. Remove a User")
        print("4. Exit")
        
        choice = input("Choose any Option. (1-4): ")
        
        if choice == '1':
            username = input("Enter the username: ")
            email = input("Enter the email: ")
            add_user(username, email)
        
        elif choice == '2':
            list_users()
        
        elif choice == '3':
            try:
                user_id = int(input("Enter the ID of the user to remove: "))
                remove_user(user_id)
            except ValueError:
                print("Please enter a valid number for the user ID.")
        
        elif choice == '4':
            print("Your Wish is my Command.")
            break
        
        else:
            print("Invalid option. Please choose a number between 1 and 4.")

# Run the program
if __name__ == "__main__":
    main()

# Close the connection to the database
conn.close()
