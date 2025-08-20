import random

# Sample product categories and products
products = {
    "soap": ["Dove Soap", "Lux Soap", "Pears Soap"],
    "mobile": ["iPhone 14", "Samsung Galaxy S23", "OnePlus 11"],
    "toys": ["Lego Set", "Barbie Doll", "Hot Wheels Car"],
    "games": ["FIFA 23", "Minecraft", "Call of Duty"],
    "shampoo": ["Head & Shoulders", "Pantene", "Clinic Plus"],
    "laptop": ["Dell Inspiron", "MacBook Air", "HP Pavilion"]
}

# User search history
user_history = []

def recommend_products(history):
    # Recommend products based on last searched category
    if not history:
        print("No search history found. Please search for a product.")
        return
    last_search = history[-1]
    if last_search in products:
        print(f"Recommended products for '{last_search}':")
        for item in products[last_search]:
            print(f"- {item}")
    else:
        # Recommend random products if category not found
        print("Category not found. Here are some popular products:")
        for cat in random.sample(list(products.keys()), 2):
            print(f"- {random.choice(products[cat])}")

def main():
    print("Welcome to the Product Recommendation System!")
    print("Type 'exit' to quit.")
    while True:
        search = input("Search for a product category: ").strip().lower()
        if search == "exit":
            print("Thank you for using the system!")
            break
        user_history.append(search)
        recommend_products(user_history)

if __name__ == "__main__":
    main()