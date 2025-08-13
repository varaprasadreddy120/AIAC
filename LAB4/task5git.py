def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 0

if __name__ == "__main__":
    file_path = r"C:\Users\P.Varaprasad Reddy\OneDrive\Desktop\kiran.txt"
    num_lines = count_lines_in_file(file_path)
    print(num_lines)