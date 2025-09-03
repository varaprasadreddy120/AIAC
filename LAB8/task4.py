import re

def is_sentence_palindrome(sentence):
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', sentence).lower()
    return cleaned == cleaned[::-1]

# Take input from user
para = input("Enter a sentence or paragraph: ")

# Print only True or False
print(is_sentence_palindrome(para))