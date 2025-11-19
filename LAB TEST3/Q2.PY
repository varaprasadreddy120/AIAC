# Q2.PY
# Linear search with early exit optimization (requires a sorted list)
def linear_search_early_exit(arr, target):
    """
    Linear search in a sorted list with early exit.
    Returns (index, comparisons) where index is -1 if not found.
    """
    comparisons = 0
    for i, value in enumerate(arr):
        comparisons += 1
        if value == target:
            return i, comparisons
        if value > target:  # early exit: remaining values are larger
            return -1, comparisons
    return -1, comparisons

def main():
    print("---- Linear Search with Early Exit Program ----")
    
    # Get list from user
    n = int(input("Enter number of elements in the list: "))
    arr = []
    print("Enter the elements (should be sorted for early exit optimization):")
    for _ in range(n):
        arr.append(int(input()))
    
    print("Array:", arr)

    # Get targets from user
    m = int(input("\nEnter number of values to search: "))
    targets = []
    print("Enter the target values:")
    for _ in range(m):
        targets.append(int(input()))
    
    print("\n---- Search Results ----")
    for t in targets:
        idx, comps = linear_search_early_exit(arr, t)
        if idx != -1:
            print(f"Target {t}: found at index {idx} (comparisons={comps})")
        else:
            print(f"Target {t}: not found (comparisons={comps})")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()