def register_user(users):
    """
    Registers a new user by asking for a username and password.
    Adds the user to the users dictionary if the username is not taken.
    """
    username = input("Enter a new username: ").strip()
    if username in users:
        print("Username already exists. Please try a different one.")
        return
    password = input("Enter a new password: ").strip()
    users[username] = password
    print("Registration successful!")

def login_user(users):
    """
    Logs in a user by checking the username and password.
    """
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    if username in users and users[username] == password:
        print("Login successful! Welcome,", username)
    else:
        print("Invalid username or password.")

def main():
    users = {}
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ").strip()
        if choice == '1':
            register_user(users)
        elif choice == '2':
            login_user(users)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
