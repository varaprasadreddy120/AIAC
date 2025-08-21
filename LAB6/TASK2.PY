def multiples(num):
    print(f"Multiples of {num} are:")
    i = 1
    while i <= 10:
        print(f"{num} x {i}= {num * i}")
        i += 1   # increase counter

# Take input first
num = int(input("Enter the number to know the first 10 multiples: "))
multiples(num)