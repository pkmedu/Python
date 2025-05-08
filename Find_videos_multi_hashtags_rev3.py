# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 07:41:45 2025

@author: muhuri
"""
# -*- coding: utf-8 -*-
"""
Modified YouTube Hashtag Video Search Tool

This script searches YouTube for videos containing multiple hashtags,
collects their links, and saves them to separate CSV files for each hashtag.
It can also open the links in your default web browser.

Requirements:
    - youtube-search-python package: pip install youtube-search-python
"""
import sys
import csv
import webbrowser
from youtubesearchpython import VideosSearch

def find_youtube_links_by_hashtag(hashtag, max_results=sys.maxsize):
    search_term = f"#{hashtag}"
    videos_search = VideosSearch(search_term, limit=20)  # Initial limit for each fetch
    
    links = []
    total_links_found = 0

    while total_links_found < max_results:
        results = videos_search.result()
        if 'result' in results:
            for video in results['result']:
                if total_links_found < max_results:
                    video_id = video.get('id')
                    if video_id:
                        link = f"https://www.youtube.com/watch?v={video_id}"
                        links.append(link)
                        total_links_found += 1
                else:
                    break  # Stop adding links once we've reached the limit

        # If we've already reached the max_results, stop fetching
        if total_links_found >= max_results:
            break

        # Try to fetch the next page of results if we haven't reached the limit
        try:
            # Check if there are more pages available
            if 'nextPageToken' in results:
                videos_search.next()  # Try to fetch the next page of results
                print(f"Fetching more results... Total links found: {total_links_found}")
            else:
                print("❌ No more results available.")
                break  # Exit the loop if no more pages are available
        except Exception as e:
            print("❌ An error occurred:", e)
            break  # Exit the loop if there's an error

    return links

def save_links_to_csv(links, hashtag, filename=None):
    if filename is None:
        # Dynamically create a filename based on hashtag
        safe_hashtag = hashtag.replace(' ', '_')
        filename = fr"c:\Data\{safe_hashtag}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        #writer.writerow([f"YouTube Links using #{hashtag}"])
        for link in links:
            writer.writerow([link])
    print(f"\n✅ Saved {len(links)} links to {filename}\n")

def open_links_in_browser(links):
    for link in links:
        webbrowser.open_new_tab(link)
    print("🚀 Opening all videos in browser tabs...")

if __name__ == "__main__":
    hashtag = input("Enter a hashtag to search (without # sign): ").strip()
    max_results_input = input("How many videos would you like to fetch? (default 10, or type 'max'): ").strip().lower()
    max_results_input = max_results_input.strip("'\"")  # Remove any accidental quotes

    if max_results_input == 'max':
        max_results = sys.maxsize
    elif max_results_input:
        try:
            max_results = int(max_results_input)
        except ValueError:
            print("❌ Invalid number entered. Using default of 10.")
            max_results = 10
    else:
        max_results = 10

    videos = find_youtube_links_by_hashtag(hashtag, max_results)

    if videos:
        save_links_to_csv(videos, hashtag)
        # If you want to automatically open links in browser, uncomment the next line:
        # open_links_in_browser(videos)
