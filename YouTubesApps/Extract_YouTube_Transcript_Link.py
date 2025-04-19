# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 14:17:29 2025

@author: muhuri
"""
# Code obtained from ChatGPT - I have slightly modified the program.
#pip install youtube-transcript-api transformers torch

from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re

def extract_video_id(url):
    match = re.search(r'(?:v=|youtu\.be/)([^&\n]+)', url)
    return match.group(1) if match else None

def get_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return None, "Invalid URL"
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = ' '.join([entry['text'] for entry in transcript])
        return full_text, None
    except Exception as e:
        return None, str(e)
# The max_length has been changed from 100 to 39
def summarize_text(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    # Split long text into smaller chunks
    max_chunk = 500
    chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    summary = ''
    for chunk in chunks:
        summary_piece = summarizer(chunk, max_length=39, min_length=30, do_sample=False)[0]['summary_text']
        summary += summary_piece + ' '
    return summary.strip()

# Example
# video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_url = "https://www.youtube.com/watch?v=qkKLYH89ShA"
transcript, error = get_transcript(video_url)

if transcript:
    print("Transcript:\n", transcript[:1000], "...\n")  # Print the first 1000 chars
    summary = summarize_text(transcript)
    print("Summary:\n", summary)
    print("Video Link:", video_url)
else:
    print("Error:", error)
#####
import os
    # Make sure the directory exists
os.makedirs("c:\\Python\\summaries", exist_ok=True)

def save_summary_txt(video_url, summary, filename="c:\\Python\\summaries\\youtube_summary.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"Video URL: {video_url}\n")
        f.write("Summary:\n")
        f.write(summary + "\n")
        f.write("=" * 80 + "\n")
    print(f"Saved summary to {os.path.abspath(filename)}")

# === Execution starts here ===
# video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_url = "https://www.youtube.com/watch?v=qkKLYH89ShA"
transcript, error = get_transcript(video_url)
if transcript:
    summary = summarize_text(transcript)
    print("Summary:\n", summary)
    print("Video Link:", video_url)
    save_summary_txt(video_url, summary)
else:
    print("Error:", error)
    
