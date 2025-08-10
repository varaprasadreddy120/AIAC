def find_largest_of_three():
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    num3 = float(input("Enter third number: "))
    largest = max(num1, num2, num3)
    return largest

# Example usage
print("The largest number is:", find_largest_of_three())