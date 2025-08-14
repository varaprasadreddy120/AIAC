def convert_temperature():
    print("Temperature Converter")
    print("Choose the conversion you want to perform:")
    print("1. Celsius to Fahrenheit")
    print("2. Celsius to Kelvin")
    print("3. Fahrenheit to Celsius")
    print("4. Fahrenheit to Kelvin")
    print("5. Kelvin to Celsius")
    print("6. Kelvin to Fahrenheit")
    
    choice = input("Enter your choice (1-6): ")
    
    if choice == '1':
        c = float(input("Enter temperature in Celsius: "))
        f = (c * 9/5) + 32
        print(f"{c} Celsius = {f} Fahrenheit")
    elif choice == '2':
        c = float(input("Enter temperature in Celsius: "))
        k = c + 273.15
        print(f"{c} Celsius = {k} Kelvin")
    elif choice == '3':
        f = float(input("Enter temperature in Fahrenheit: "))
        c = (f - 32) * 5/9
        print(f"{f} Fahrenheit = {c} Celsius")
    elif choice == '4':
        f = float(input("Enter temperature in Fahrenheit: "))
        k = (f - 32) * 5/9 + 273.15
        print(f"{f} Fahrenheit = {k} Kelvin")
    elif choice == '5':
        k = float(input("Enter temperature in Kelvin: "))
        c = k - 273.15
        print(f"{k} Kelvin = {c} Celsius")
    elif choice == '6':
        k = float(input("Enter temperature in Kelvin: "))
        f = (k - 273.15) * 9/5 + 32
        print(f"{k} Kelvin = {f} Fahrenheit")
    else:
        print("Invalid choice. Please select a number between 1 and 6.")

convert_temperature()
