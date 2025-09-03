class ShoppingCart:
    def __init__(self):  # Fixed constructor name
        self.cart = []

    def add_to_cart(self, item):
        self.cart.append(item)
        print(f"Added '{item}' to cart.")

    def remove_from_cart(self, item):
        if item in self.cart:
            self.cart.remove(item)
            print(f"Removed '{item}' from cart.")
        else:
            print(f"Item '{item}' not found in cart.")

    def view_cart(self):
        if not self.cart:
            print("Your cart is empty.")
        else:
            print("Items in your cart:")
            for idx, item in enumerate(self.cart, 1):
                print(f"{idx}. {item}")


def main():
    shop_items = ['Laptop', 'Smartphone', 'Headphones', 'Tablet', 'Smartwatch']
    cart = ShoppingCart()

    while True:
        print("\nAvailable items:", ', '.join(shop_items))
        print("Options: [1] Add to cart  [2] Remove from cart  [3] View cart  [4] Exit")
        choice = input("Select an option: ")

        if choice == '1':
            item = input("Enter item to add: ")
            if item in shop_items:
                cart.add_to_cart(item)
            else:
                print("Item not available.")
        elif choice == '2':
            item = input("Enter item to remove: ")
            cart.remove_from_cart(item)
        elif choice == '3':
            cart.view_cart()
        elif choice == '4':
            print("Thank you for shopping!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":  # Fixed entry point
    main()