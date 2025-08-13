def format_full_name():
    full_name = input("Enter full name: ").strip()
    parts = full_name.split()
    if len(parts) < 2:
        print("Please enter at least first and last name.")
        return
    last_name = parts[0]
    first_name = ' '.join(parts[1:])
    print(f"last name: {last_name}")
    print(f"First name: {first_name}")

# Example usage
format_full_name()