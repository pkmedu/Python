# -*- coding: utf-8 -*-
"""
Created on Sun Apr 20 06:18:33 2025

@author: muhuri
"""
#import re
import json
import textwrap
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs



# ========== Constants ==========
MAX_LENGTH = 300  # For summary output
MIN_LENGTH = 100
WRAP_WIDTH = 100
TXT_OUTPUT = "summary_output.txt"
JSON_OUTPUT = "summary_output.json"


# ========== Functions ==========

def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed_url.query)["v"][0]
    elif parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    else:
        raise ValueError("Unsupported YouTube URL format.")


#def get_transcript(video_id):
#    transcript = YouTubeTranscriptApi.get_transcript(video_id)
#    full_text = " ".join([entry["text"] for entry in transcript])
#    return full_text

def get_transcript(video_id):
    try:
        raw_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        cleaned_lines = [entry['text'].replace('\n', ' ').strip() for entry in raw_transcript]
        full_transcript = ' '.join(cleaned_lines)
        return full_transcript
    except Exception as e:
        print(f"Failed to fetch transcript for {video_id}: {e}")
        return None

def split_text(text, max_chunk_len=1000):
    words = text.split()
    chunks = []
    chunk = []

    for word in words:
        if sum(len(w) + 1 for w in chunk) + len(word) + 1 <= max_chunk_len:
            chunk.append(word)
        else:
            chunks.append(" ".join(chunk))
            chunk = [word]
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks

def summarize_chunks(chunks, summarizer):
    summaries = []
    for i, chunk in enumerate(chunks):
        input_length = len(chunk.split())
        # Allow summary to be ~50% of input length or max 300
        max_len = min(int(input_length * 0.6), 300)
        min_len = min(int(input_length * 0.3), max_len - 1)

        print(f"🔍 Summarizing chunk {i + 1}/{len(chunks)}... (input_length={input_length}, max_len={max_len})")
        try:
            result = summarizer(
                chunk,
                max_length=max_len,
                min_length=min_len,
                do_sample=False
            )
            summaries.append(result[0]["summary_text"])
        except Exception as e:
            print(f"❌ Error summarizing chunk {i + 1}: {e}")
            summaries.append("[Summary Failed]")
    return " ".join(summaries)


def save_outputs(url, transcript, summary):
    # Save TXT
    with open(TXT_OUTPUT, "w", encoding="utf-8") as f:
        f.write("🔗 URL:\n" + url + "\n\n")
        f.write("📜 TRANSCRIPT:\n")
        f.write(textwrap.fill(transcript, width=WRAP_WIDTH) + "\n\n")
        f.write("📝 SUMMARY:\n")
        f.write(textwrap.fill(summary, width=WRAP_WIDTH))


   # Strip any extra whitespace from the transcript
    transcript = transcript.strip()

   # Prepare final dictionary for saving to JSON
    data = {
        "url": url,  # Or use `video_url` if that's the correct variable
        "transcript": textwrap.fill(transcript, width=WRAP_WIDTH),
        "summary": textwrap.fill(summary, width=WRAP_WIDTH)
    }

    # Save to JSON file
    with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# ========== Main ==========
def main():
    # Example URL: replace this or pass it dynamically
    video_url = "https://www.youtube.com/watch?v=1Tg9i_wpH80"
    print("📥 Getting transcript...")

    video_id = extract_video_id(video_url)
    full_transcript = get_transcript(video_id)

    print("✂️ Splitting transcript into chunks...")
    chunks = split_text(full_transcript)

    print("🧠 Summarizing...")
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

    summary = summarize_chunks(chunks, summarizer)

    print("💾 Saving output...")
    save_outputs(video_url, full_transcript, summary)

    print("✅ Done! Files saved:")
    print("  -", TXT_OUTPUT)
    print("  -", JSON_OUTPUT)


if __name__ == "__main__":
    main()

