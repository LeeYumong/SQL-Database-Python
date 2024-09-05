import sqlite3
from datetime import datetime

# Connect to the SQLite database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Execute the schema to create the table
with open('user_data_schema.sql', 'r') as f:
    cursor.executescript(f.read())
conn.commit()

# Function to add a new user
def add_user(username, email):
    try:
        cursor.execute('''
        INSERT INTO User (username, email)
        VALUES (?, ?)
        ''', (username, email))
        conn.commit()
        print(f"User '{username}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"User '{username}' or email '{email}' already exists.")

# Function to retrieve all users
def get_users():
    cursor.execute('SELECT * FROM User')
    users = cursor.fetchall()
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}, Created At: {user[3]}")

# Function to delete a user by ID
def delete_user(user_id):
    cursor.execute('DELETE FROM User WHERE id = ?', (user_id,))
    conn.commit()
    print(f"User with ID {user_id} deleted successfully.")

def main():
    print("Adding users...")
    add_user('alice', 'alice@example.com')
    add_user('bob', 'bob@example.com')
    
    print("\nRetrieving all users...")
    get_users()

    print("\nDeleting a user...")
    delete_user(1)  # Adjust the ID based on the actual data

    print("\nRetrieving all users after deletion...")
    get_users()

if __name__ == "__main__":
    main()

# Close the database connection
conn.close()
