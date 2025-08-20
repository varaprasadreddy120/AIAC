def collect_user_data():
    name = input("Enter your name: ")
    age = input("Enter your age: ")
    email = input("Enter your email: ")
    ph_num = input("Enter your phone number: ")
    address = input("Enter your address: ")

    data = (
        f"Name: {name}\n"
        f"Age: {age}\n"
        f"Email: {email}\n"
        f"Phone Number: {ph_num}\n"
        f"Address: {address}\n"
    )

    with open("user_data.txt", "w") as file:
        file.write(data)
    print("User data saved to user_data.txt")

if __name__ == "__main__":
    collect_user_data()