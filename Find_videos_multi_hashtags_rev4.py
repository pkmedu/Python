# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 23:30:47 2025

@author: muhuri
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 07:41:45 2025
@author: muhuri

Modified YouTube Hashtag Video Search Tool
This script searches YouTube for videos containing multiple hashtags,
collects their links, and saves them to separate CSV files for each hashtag.
It can also open the links in your default web browser.

Requirements:
    - youtube-search-python package: pip install youtube-search-python
"""
import sys
import csv
import os
import webbrowser
from youtubesearchpython import VideosSearch

def find_youtube_links_by_hashtag(hashtag, max_results=sys.maxsize):
    """
    Search YouTube for videos with a specific hashtag and return links.
    
    Args:
        hashtag (str): The hashtag to search for (without the # symbol).
        max_results (int): Maximum number of results to return.
        
    Returns:
        list: List of YouTube video links.
    """
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
            # Check if we can get more results
            has_next = videos_search.next()
            if has_next:
                print(f"Fetching more results... Total links found: {total_links_found}")
            else:
                print("❌ No more results available.")
                break  # Exit the loop if no more pages are available
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            break  # Exit the loop if there's an error
    
    return links

def save_links_to_csv(links, hashtag, filename=None):
    """
    Save the collected YouTube links to a CSV file.
    
    Args:
        links (list): List of YouTube video links.
        hashtag (str): The hashtag used for the search.
        filename (str, optional): Custom filename to save to. If None, a filename is generated.
    """
    if filename is None:
        # Dynamically create a filename based on hashtag
        safe_hashtag = hashtag.replace(' ', '_')
        # Create directory if it doesn't exist
        os.makedirs("c:\\Data", exist_ok=True)
        filename = fr"c:\Data\{safe_hashtag}.csv"
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([f"YouTube Links using #{hashtag}"])
        for link in links:
            writer.writerow([link])
    
    print(f"\n✅ Saved {len(links)} links to {filename}\n")

def open_links_in_browser(links, max_tabs=5):
    """
    Open YouTube links in the default web browser.
    
    Args:
        links (list): List of YouTube video links to open.
        max_tabs (int): Maximum number of tabs to open at once (to avoid browser overload).
    """
    if len(links) > max_tabs:
        confirm = input(f"⚠️ This will open {len(links)} tabs. Continue? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Operation cancelled.")
            return

    for i, link in enumerate(links):
        webbrowser.open_new_tab(link)
        if i >= max_tabs - 1:
            break
    
    print(f"🚀 Opened {min(len(links), max_tabs)} videos in browser tabs...")

def main():
    """Main function to run the YouTube hashtag search tool."""
    print("🔍 YouTube Hashtag Video Search Tool 🔍")
    print("======================================")
    
    # Get hashtag input
    hashtag = input("Enter a hashtag to search (without # sign): ").strip()
    while not hashtag:
        print("Hashtag cannot be empty.")
        hashtag = input("Enter a hashtag to search (without # sign): ").strip()
    
    # Get max results
    max_results_input = input("How many videos would you like to fetch? (default 10, or type 'max'): ").strip().lower()
    max_results_input = max_results_input.strip("'\"")  # Remove any accidental quotes
    
    if max_results_input == 'max':
        max_results = sys.maxsize
    elif max_results_input:
        try:
            max_results = int(max_results_input)
            if max_results <= 0:
                print("❌ Number must be positive. Using default of 10.")
                max_results = 10
        except ValueError:
            print("❌ Invalid number entered. Using default of 10.")
            max_results = 10
    else:
        max_results = 10
    
    print(f"\nSearching for videos with #{hashtag}...")
    videos = find_youtube_links_by_hashtag(hashtag, max_results)
    
    if videos:
        print(f"\n🎉 Found {len(videos)} videos with #{hashtag}")
        save_links_to_csv(videos, hashtag)
        
        # Ask if user wants to open links
        open_browser = input("Would you like to open some videos in your browser? (y/n): ").strip().lower()
        if open_browser == 'y':
            open_links_in_browser(videos)
    else:
        print(f"❌ No videos found with #{hashtag}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
    finally:
        input("\nPress Enter to exit...")