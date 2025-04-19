# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 04:29:35 2025

@author: muhuri
"""
# pip install --upgrade torch transformers

import re
import os
import sys
import textwrap
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# === Extract YouTube video ID ===
def extract_video_id(url):
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|$)', url)
    return match.group(1) if match else None

# === Retrieve transcript using video ID ===
def get_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None, "Invalid YouTube URL."
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([entry['text'] for entry in transcript])
        return full_text, None
    except Exception as e:
        return None, str(e)

# === Split long text into manageable chunks ===
def chunk_text(text, max_length=500):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ''

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_length:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# === Summarize text using Hugging Face Transformers ===
def summarize_text(text, min_len=40, max_len=80):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    chunks = chunk_text(text)
    summary = ''
    
    for i, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {i}/{len(chunks)}...")
        if len(chunk.split()) < min_len:
            summary += chunk + ' '  # Use original text for very short chunks
            continue
        result = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)
        summary += result[0]['summary_text'] + ' '

    return summary.strip()

# === Save output to a file ===
def save_summary_txt(video_url, summary, transcript, filename="Stharoor_summary.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== Transcript ===\n")
        for line in transcript.splitlines():
            f.write(textwrap.fill(line, width=80) + "\n")

        f.write("\n=== Characters Per Line ===\n")
        for i, line in enumerate(transcript.splitlines(), start=1):
            f.write(f"Line {i:>2}: {len(line)} characters\n")

        f.write("\n=== Summary ===\n")
        f.write(textwrap.fill(summary, width=80) + "\n")

        f.write("\n=== Video Link ===\n")
        f.write(video_url + "\n")

# === Main Program ===
if __name__ == "__main__":
    # Usage: python script.py <video_url> [min_len] [max_len]
    video_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.youtube.com/watch?v=330hPz8iLi4"
    MIN_LENGTH = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    MAX_LENGTH = int(sys.argv[3]) if len(sys.argv) > 3 else 50

    transcript, error = get_transcript(video_url)

    if transcript and transcript.strip():
        summary = summarize_text(transcript, min_len=MIN_LENGTH, max_len=MAX_LENGTH)

        print("\n=== Transcript ===")
        print(transcript)

        print("\n=== Summary ===")
        print(summary)

        print("\n=== Video Link ===")
        print(video_url)

        save_summary_txt(video_url, summary, transcript, filename="Stharoor_summary.txt")

    else:
        print("❌ Transcript not available.")
        print("Reason:", error)
