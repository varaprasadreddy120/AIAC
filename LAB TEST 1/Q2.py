# Take input from the user
numbers = input("Enter numbers separated by spaces: ")

# Convert input string to a list of integers
num_list = list(map(int, numbers.split()))

# Remove duplicates using set and sort the result
unique_sorted = sorted(set(num_list))

# Print the sorted result
print(' '.join(map(str, unique_sorted)))