# app.py
import streamlit as st
from chat_parser import parse_chat_folder

st.title("AI Chat Log Summarizer")

if st.button("Summarize Folder"):
    folder_path = r"C:\Users\ASUS\Desktop\QTec Task\input folder"
    summary = parse_chat_folder(folder_path)
    st.text_area("Summary", summary, height=400)
