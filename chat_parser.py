{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 33,
   "id": "146b578e-2016-4ba4-892b-368286f1852b",
   "metadata": {},
   "outputs": [],
   "source": [
    "import re\n",
    "import string\n",
    "from collections import Counter\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "a8b99e4c-ff22-4d60-9e34-4351312172fb",
   "metadata": {},
   "outputs": [],
   "source": [
    "def load_chat_log(file_path):\n",
    "    with open(file_path, 'r', encoding='utf-8') as file:\n",
    "        lines = file.readlines()\n",
    "\n",
    "    user_msgs = []\n",
    "    ai_msgs = []\n",
    "\n",
    "    for line in lines:\n",
    "        if line.startswith(\"User:\"):\n",
    "            user_msgs.append(line[len(\"User:\"):].strip())\n",
    "        elif line.startswith(\"AI:\"):\n",
    "            ai_msgs.append(line[len(\"AI:\"):].strip())\n",
    "\n",
    "    return user_msgs, ai_msgs\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "id": "b1e4677e-74af-42c3-8690-cf5cd9f62fd1",
   "metadata": {},
   "outputs": [],
   "source": [
    "def preprocess_text(messages):\n",
    "    combined_text = ' '.join(messages).lower()\n",
    "    combined_text = combined_text.translate(str.maketrans('', '', string.punctuation))\n",
    "    return combined_text\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "8e2e1bea-48dd-4800-9014-7bab33bfb740",
   "metadata": {},
   "outputs": [],
   "source": [
    "def extract_keywords_tfidf(text, top_n=5):\n",
    "    vectorizer = TfidfVectorizer(stop_words='english')\n",
    "    tfidf_matrix = vectorizer.fit_transform([text])\n",
    "    tfidf_scores = tfidf_matrix.toarray()[0]\n",
    "    feature_names = vectorizer.get_feature_names_out()\n",
    "\n",
    "    # Pair words with their scores\n",
    "    word_scores = list(zip(feature_names, tfidf_scores))\n",
    "    sorted_words = sorted(word_scores, key=lambda x: x[1], reverse=True)\n",
    "    \n",
    "    return [word for word, score in sorted_words[:top_n]]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "85d5c728-3859-4284-ae70-067c5c88ccbc",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Custom conversational stopwords\n",
    "CONVERSATIONAL_STOPWORDS = {\n",
    "    'hi', 'hello', 'bye', 'goodbye', 'thanks', 'thank', 'okay', 'ok', 'sure',\n",
    "    'yeah', 'yes', 'no', 'please', 'welcome', 'well', 'alright'\n",
    "}\n",
    "\n",
    "# Extract keywords using TF-IDF and remove conversational fillers\n",
    "def extract_keywords_tfidf(text, top_n=5):\n",
    "    vectorizer = TfidfVectorizer(stop_words='english')\n",
    "    tfidf_matrix = vectorizer.fit_transform([text])\n",
    "    tfidf_scores = tfidf_matrix.toarray()[0]\n",
    "    feature_names = vectorizer.get_feature_names_out()\n",
    "    word_scores = list(zip(feature_names, tfidf_scores))\n",
    "\n",
    "    # Filter out conversational fillers\n",
    "    filtered_words = [(word, score) for word, score in word_scores if word.lower() not in CONVERSATIONAL_STOPWORDS]\n",
    "    sorted_words = sorted(filtered_words, key=lambda x: x[1], reverse=True)\n",
    "\n",
    "    return [word for word, _ in sorted_words[:top_n]]\n",
    "\n",
    "# Generate the full summary\n",
    "def generate_summary(file_name, user_msgs, ai_msgs, keywords):\n",
    "    total_msgs = len(user_msgs) + len(ai_msgs)\n",
    "    \n",
    "    # Heuristic topic sentence\n",
    "    if keywords:\n",
    "        topic_phrase = ', '.join(keywords[:1])\n",
    "        topic_line = f\"The user asked mainly about {topic_phrase} and related topics.\"\n",
    "    else:\n",
    "        topic_line = \"The nature of the conversation could not be determined.\"\n",
    "\n",
    "    # Final formatted output\n",
    "    print(f\"\\nSummary for {file_name}:\")\n",
    "    print(f\"- The conversation had {total_msgs} exchanges.\")\n",
    "    print(f\"- {topic_line}\")\n",
    "    print(f\"- Most common keywords: {', '.join(keywords)}\")\n",
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 38,
   "id": "b33a2239-9ddf-4c1c-936c-a47ef3c39279",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Process all .txt files in a folder\n",
    "def process_folder(folder_path):\n",
    "    for filename in os.listdir(folder_path):\n",
    "        if filename.endswith(\".txt\"):\n",
    "            file_path = os.path.join(folder_path, filename)\n",
    "            user_msgs, ai_msgs = load_chat_log(file_path)\n",
    "            combined_msgs = user_msgs + ai_msgs\n",
    "            cleaned_text = preprocess_text(combined_msgs)\n",
    "            keywords = extract_keywords_tfidf(cleaned_text)\n",
    "            generate_summary(filename, user_msgs, ai_msgs, keywords)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "10403b52-bb6f-479e-a772-cebd17790b64",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "Summary for chat1.txt:\n",
      "- The conversation had 8 exchanges.\n",
      "- The user asked mainly about python and related topics.\n",
      "- Most common keywords: python, learning, machine, use, ai\n",
      "\n",
      "Summary for chat2.txt:\n",
      "- The conversation had 4 exchanges.\n",
      "- The user asked mainly about python and related topics.\n",
      "- Most common keywords: python, use, web, analysis, data\n"
     ]
    }
   ],
   "source": [
    "import os\n",
    "\n",
    "# Run for all chat logs in the folder\n",
    "if __name__ == \"__main__\":\n",
    "    folder_path = \"input folder\"  # change this to your folder name\n",
    "    process_folder(folder_path)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "829ba5a4-e082-4a68-b50f-be2c03c4549f",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
