# Q1.PY
# Binary Search Tree implementation with insert, inorder traversal, and search
# Demonstration with sample input when run as a script

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        """Insert key into BST."""
        if self.root is None:
            self.root = Node(key)
            return

        current = self.root
        while True:
            if key < current.key:
                if current.left is None:
                    current.left = Node(key)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(key)
                    return
                current = current.right

    def inorder(self):
        """Return inorder traversal as a list (sorted order for BST)."""
        result = []
        def _inorder(node):
            if node is None:
                return
            _inorder(node.left)
            result.append(node.key)
            _inorder(node.right)
        _inorder(self.root)
        return result

    def search(self, key):
        """Search for key in BST. Return the node if found, else None."""
        current = self.root
        while current is not None:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None

if __name__ == "__main__":
    print("---- Binary Search Tree Program ----")
    
    # Get values from user
    n = int(input("Enter number of values to insert: "))
    values_to_insert = []
    print("Enter the values:")
    for _ in range(n):
        value = int(input())
        values_to_insert.append(value)
    
    bst = BinarySearchTree()
    for v in values_to_insert:
        bst.insert(v)

    print("\nInserted values:", values_to_insert)
    print("Inorder traversal (sorted):", bst.inorder())

    # Get keys to search from user
    m = int(input("\nEnter number of values to search: "))
    keys_to_search = []
    print("Enter the values to search:")
    for _ in range(m):
        key = int(input())
        keys_to_search.append(key)
    
    print("\n---- Search Results ----")
    for k in keys_to_search:
        node = bst.search(k)
        if node:
            print(f"Search {k}: Found node with key = {node.key}")
        else:
            print(f"Search {k}: Not found")