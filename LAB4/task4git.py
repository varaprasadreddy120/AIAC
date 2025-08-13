# Program to count the number of vowels in a given string

def count_vowels(s):
    vowels = 'aeiouAEIOU'
    return sum(1 for char in s if char in vowels)

user_input = input("Enter a string: ")
vowel_count = count_vowels(user_input)
print(f"Number of vowels in the given string: {vowel_count}")

def detailed_vowel_count(s):
    vowels = 'aeiouAEIOU'
    count_dict = {}
    for char in s:
        if char in vowels:
            lower_char = char.lower()
            count_dict[lower_char] = count_dict.get(lower_char, 0) + 1
    total_vowels = sum(count_dict.values())
    details = ', '.join(f"{v}’s" if count > 1 else f"{v}" for v, count in count_dict.items())
    details = ', '.join(f"{count}{v}’s" if count > 1 else f"{count}{v}" for v, count in count_dict.items())
    print(f"The number of vowels present in given string are : {total_vowels}vowels({details})")

# Example usage:
detailed_vowel_count(user_input)