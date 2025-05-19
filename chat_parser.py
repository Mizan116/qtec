import os
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter

# Download stopwords once
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))
conversational_fillers = {'hi', 'hello', 'bye', 'thanks', 'thank', 'ok', 'okay'}

def clean_text(text):
    return re.findall(r'\b[a-z]+\b', text.lower())

def extract_keywords(messages, top_n=5):
    words = []
    for message in messages:
        words.extend(clean_text(message))
    filtered = [w for w in words if w not in stop_words and w not in conversational_fillers]
    most_common = Counter(filtered).most_common(top_n)
    return [word for word, _ in most_common]

def parse_chat_file(file_path):
    user_msgs, ai_msgs = [], []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('User:'):
                user_msgs.append(line[len('User:'):].strip())
            elif line.startswith('AI:'):
                ai_msgs.append(line[len('AI:'):].strip())

    total = len(user_msgs) + len(ai_msgs)
    keywords = extract_keywords(user_msgs + ai_msgs)
    conversation_nature = ', '.join(keywords) if keywords else "general"

    summary = f"""Summary for {os.path.basename(file_path)}:
- The conversation had {total} exchanges.
- The user asked mainly about {conversation_nature}.
- Most common keywords: {', '.join(keywords)}."""
    
    return summary

def parse_chat_folder(folder_path):
    summaries = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            summaries.append(parse_chat_file(file_path))
    return "\n\n".join(summaries)
