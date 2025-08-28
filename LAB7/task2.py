def sort_list(data):
    return sorted(data, key=str)

items = [3, "apple", 1, "banana", 2]
sorted_items = sort_list(items)
print("Sorted items:", sorted_items)
