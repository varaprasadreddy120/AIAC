import re
import hashlib

def mask_email(email):
    # Mask email except first and last character before @
    parts = email.split('@')
    if len(parts[0]) > 2:
        masked = parts[0][0] + '*'*(len(parts[0])-2) + parts[0][-1]
    else:
        masked = parts[0][0] + '*'
    return masked + '@' + parts[1]

def mask_phone(phone):
    # Mask all but last 2 digits
    return '*'*(len(phone)-2) + phone[-2:]

def hash_data(data):
    # Hash sensitive data
    return hashlib.sha256(data.encode()).hexdigest()

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\d{10}$", phone)

name = input("Enter your name: ")
age = input("Enter your age: ")
email = input("Enter your email: ")
while not is_valid_email(email):
    email = input("Invalid email. Enter again: ")
ph_num = input("Enter your phone number (10 digits): ")
while not is_valid_phone(ph_num):
    ph_num = input("Invalid phone number. Enter again: ")
address = input("Enter your address: ")

# Mask and hash sensitive data
masked_email = mask_email(email)
masked_ph_num = mask_phone(ph_num)
hashed_email = hash_data(email)
hashed_ph_num = hash_data(ph_num)

data = (
    f"Name: {name}\n"
    f"Age: {age}\n"
    f"Email (masked): {masked_email}\n"
    f"Email (hashed): {hashed_email}\n"
    f"Phone (masked): {masked_ph_num}\n"
    f"Phone (hashed): {hashed_ph_num}\n"
    f"Address: {address}\n"
)

with open("user_data.txt", "w") as file:
    file.write(data)

print("User data saved securely to user_data.txt.")