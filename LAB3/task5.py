def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15

def fahrenheit_to_kelvin(fahrenheit):
    """Convert Fahrenheit to Kelvin."""
    return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))

def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit."""
    return celsius_to_fahrenheit(kelvin_to_celsius(kelvin))

def main():
    print("Temperature Conversion Program")
    print("-----------------------------")
    print("Choose the conversion type:")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Celsius to Kelvin")
    print("4. Kelvin to Celsius")
    print("5. Fahrenheit to Kelvin")
    print("6. Kelvin to Fahrenheit")
    print("7. Exit")

    while True:
        choice = input("\nEnter your choice (1-7): ").strip()
        if choice == '1':
            c = float(input("Enter temperature in Celsius: "))
            f = celsius_to_fahrenheit(c)
            print(f"{c}°C = {f:.2f}°F")
        elif choice == '2':
            f = float(input("Enter temperature in Fahrenheit: "))
            c = fahrenheit_to_celsius(f)
            print(f"{f}°F = {c:.2f}°C")
        elif choice == '3':
            c = float(input("Enter temperature in Celsius: "))
            k = celsius_to_kelvin(c)
            print(f"{c}°C = {k:.2f}K")
        elif choice == '4':
            k = float(input("Enter temperature in Kelvin: "))
            c = kelvin_to_celsius(k)
            print(f"{k}K = {c:.2f}°C")
        elif choice == '5':
            f = float(input("Enter temperature in Fahrenheit: "))
            k = fahrenheit_to_kelvin(f)
            print(f"{f}°F = {k:.2f}K")
        elif choice == '6':
            k = float(input("Enter temperature in Kelvin: "))
            f = kelvin_to_fahrenheit(k)
            print(f"{k}K = {f:.2f}°F")
        elif choice == '7':
            print("Thank you for using the Temperature Conversion Program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
