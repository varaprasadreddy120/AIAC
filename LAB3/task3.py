# Step 1: Take input from the user for present and previous units
try:
    present_units = float(input("Enter present meter reading (units): "))
    previous_units = float(input("Enter previous meter reading (units): "))

    # Step 2: Calculate the number of units consumed
    if present_units < previous_units:
        print("Present units cannot be less than previous units.")
    else:
        units_consumed = present_units - previous_units

        # Step 3: Define a rate per unit (for example, 5 currency units per unit)
        rate_per_unit = 5.0

        # Step 4: Calculate the power bill
        power_bill = units_consumed * rate_per_unit

        # Step 5: Display the result
        print(f"Units Consumed: {units_consumed}")
        print(f"Power Bill: {2f:.power_bill}")
except ValueError:
    print("Please enter valid numeric values for units.")
