def count_vowels():
    text = input("Enter a string: ")
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    print(f"Number of vowels: {count}")

count_vowels()

def detailed_vowel_count():
    text = input("Enter the string: ")
    vowels = "aeiouAEIOU"
    vowel_counts = {}
    total = 0
    for char in text:
        if char in vowels:
            total += 1
            key = char.lower()
            vowel_counts[key] = vowel_counts.get(key, 0) + 1
    if total == 0:
        print("The number of vowels present in given string are : 0 vowels")
        return
    details = []
    for v in "aeiou":
        if v in vowel_counts:
            count = vowel_counts[v]
            if count == 1:
                details.append(f"1{v}")
            else:
                details.append(f"{count}{v}'s")
    details_str = ", ".join(details)
    print(f"The number of vowels present in given string are : {total}vowels({details_str})")

detailed_vowel_count()
