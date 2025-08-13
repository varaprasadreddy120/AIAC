file_path = r"C:\Users\P.Varaprasad Reddy\OneDrive\Desktop\kiran.txt"

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        line_count = sum(1 for _ in file)
    print(line_count)
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
