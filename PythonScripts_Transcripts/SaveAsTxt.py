# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 16:02:37 2025

@author: muhuri
"""

import os

# === Execution starts here ===
video_url = "https://www.youtube.com/watch?v=5MgBikgcWnY"  # Try with a working video

transcript, error = get_transcript(video_url)

if transcript:
    summary = summarize_text(transcript)
    
    print("=== Summarised Text (Transcript) ===")
    print(transcript[:1000], "...")  # Optional: preview only first 1000 chars

    print("\n=== Summary ===")
    print(summary)

    print("\n=== Video Link ===")
    print(video_url)

    # Save all three into file
    def save_summary_txt(video_url, summary, full_text, filename="c:\\Python\\summaries\\youtube_summary.txt"):
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"Video URL: {video_url}\n")
            f.write("\nSummarised Text (Transcript):\n")
            f.write(full_text + "\n")
            f.write("\nSummary:\n")
            f.write(summary + "\n")
            f.write("=" * 80 + "\n")
        print(f"Saved summary to {os.path.abspath(filename)}")

    save_summary_txt(video_url, summary, transcript)

else:
    print("❌ Transcript not available.")
    print("Reason:", error)
