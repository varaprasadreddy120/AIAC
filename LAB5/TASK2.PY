import sys

def analyze_sentiment(text):
    positive_words = {'awesome', 'excellent', 'good', 'great', 'fantastic', 'amazing', 'love', 'wonderful', 'positive', 'happy'}
    negative_words = {'bad', 'terrible', 'awful', 'poor', 'hate', 'worst', 'negative', 'sad', 'disappointing', 'horrible'}

    text_lower = text.lower()
    pos_count = sum(word in text_lower for word in positive_words)
    neg_count = sum(word in text_lower for word in negative_words)

    if pos_count > neg_count:
        sentiment = 'positive'
    elif neg_count > pos_count:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    return sentiment

if __name__ == "__main__":
    user_input = input("Enter your sentence: ")
    sentiment = analyze_sentiment(user_input)
    print(f"Sentiment: {sentiment}")