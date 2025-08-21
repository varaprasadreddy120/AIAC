def sum_first_n_numbers(n):
    total = 0
    i = 1
    while i <= n:
        total += i
        i += 1
    return total

n = int(input("Enter the value of n: "))
result = sum_first_n_numbers(n)
print(f"Sum of first {n} numbers is {result}")