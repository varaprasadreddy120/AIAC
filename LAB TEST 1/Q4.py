def clean_text():
    import string

    # Define a simple list of English stop words
    stop_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'if', 'while', 'with', 'to', 'of', 'at', 'by', 'for', 'from', 'in', 'on', 'off', 'out', 'over', 'under', 'as', 'is', 'it', 'this', 'that', 'these', 'those', 'am', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'so', 'such'
    }

    text = input("Enter your text: ")

    # Remove punctuation
    text_no_punct = text.translate(str.maketrans('', '', string.punctuation))

    # Convert to lowercase
    text_lower = text_no_punct.lower()

    # Remove stop words
    words = text_lower.split()
    filtered_words = [word for word in words if word not in stop_words]

    cleaned_text = ' '.join(filtered_words)
    print("Cleaned text:", cleaned_text)

clean_text()
