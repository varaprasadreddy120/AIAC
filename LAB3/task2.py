numbers = input("Enter numbers separated by spaces: ")
num_list = [int(num) for num in numbers.split()]
num_list.sort(reverse=True)
print("Sorted numbers in descending order:", num_list)
