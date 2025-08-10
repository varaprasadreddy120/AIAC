def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def main():
    try:
        num = int(input("Enter a non-negative integer: "))
        if num < 0:
            print("Factorial is not defined for negative numbers.")
        else:
            print(f"Factorial of {num} is {factorial(num)}")
    except ValueError:
        print("Please enter a valid integer.")

if __name__ == "__main__":
    main()


    def factorial_from_input():
        try:
            num = int(input("Enter a non-negative integer for factorial: "))
            if num < 0:
                print("Factorial is not defined for negative numbers.")
            else:
                print(f"Factorial of {num} is {factorial(num)}")
        except ValueError:
            print("Please enter a valid integer.")


            def factorial_with_while():
                try:
                    num = int(input("Enter a non-negative integer for factorial (while loop): "))
                    if num < 0:
                        print("Factorial is not defined for negative numbers.")
                        return
                    result = 1
                    i = 2
                    while i <= num:
                        result *= i
                        i += 1
                    print(f"Factorial of {num} is {result}")
                except ValueError:
                    print("Please enter a valid integer.")
