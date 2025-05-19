# AI Chat Log Summarizer

## Project Overview
This Python-based tool reads chat logs between a user and an AI from `.txt` files, parses the conversations, and generates a summary that includes message statistics and frequently used keywords. The tool uses basic NLP techniques and optionally a TF-IDF approach for keyword extraction.

## Features
- Parses chat logs separating messages by speaker (User and AI).
- Counts total messages and messages per speaker.
- Extracts top 5 keywords excluding common stopwords and conversational fillers.
- Generates a natural language summary including:
  - Total number of exchanges.
  - Nature of the conversation based on keywords.
  - Most common keywords.
- Optional: Supports summarizing multiple chat logs from a folder.

## Requirements
- Python 3.6 or higher
- Libraries: `nltk`, `scikit-learn`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-chat-log-summarizer.git
   cd ai-chat-log-summarizer
