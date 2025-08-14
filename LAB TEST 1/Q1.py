# Take input from the user
numbers = input("Enter numbers separated by spaces: ").split()

# Convert input strings to integers
numbers = [int(num) for num in numbers]

# Initialize sums
even_sum = 0
odd_sum = 0

# Calculate sums
for num in numbers:
    if num % 2 == 0:
        even_sum += num
    else:
        odd_sum += num

# Display results
print("Sum of even numbers:", even_sum)
print("Sum of odd numbers:", odd_sum)