# ...existing code...
def factorial(n):
    """Return n! using recursion. Raises on invalid input."""
    if not isinstance(n, int):
        raise TypeError("factorial() only accepts integers")
    if n < 0:
        raise ValueError("factorial() not defined for negative values")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

if __name__ == "__main__":
    try:
        s = input("Enter a non-negative integer (or press Enter to run demo for 5 and 0): ").strip()
        if s == "":
            # Demo calls when user presses Enter
            for demo_n in (5, 0):
                print(f"{demo_n}! = {factorial(demo_n)}")
        else:
            n = int(s)
            if n < 0:
                print("Error: please enter a non-negative integer.")
            else:
                print(f"{n}! = {factorial(n)}")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
    except RecursionError:
        print("Error: recursion depth exceeded for this input.")
# ...existing code...