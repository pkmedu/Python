# -*- coding: utf-8 -*-
"""
Created on Thu May  8 05:35:42 2025

@author: muhuri
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Improved YouTube Hashtag Video Search Tool

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
from pathlib import Path
from datetime import datetime, timedelta
import re

try:
    from youtubesearchpython import VideosSearch
except ImportError:
    print("Error: Required package not found. Please install with:")
    print("pip install youtube-search-python")
    sys.exit(1)

def convert_relative_to_absolute_date(relative_date):
    """
    Convert relative date strings from YouTube (e.g., '2 weeks ago') to absolute dates.
    
    Args:
        relative_date (str): Relative date string from YouTube
        
    Returns:
        str: Absolute date in YYYY-MM-DD format
    """
    if not relative_date or relative_date == 'Unknown Date':
        return 'Unknown Date'
        
    today = datetime.now()
    
    # Common relative date patterns
    patterns = [
        # Hours ago
        (r'(\d+)\s+hour[s]?\s+ago', lambda x: today - timedelta(hours=int(x.group(1)))),
        # Days ago
        (r'(\d+)\s+day[s]?\s+ago', lambda x: today - timedelta(days=int(x.group(1)))),
        # Weeks ago
        (r'(\d+)\s+week[s]?\s+ago', lambda x: today - timedelta(weeks=int(x.group(1)))),
        # Months ago
        (r'(\d+)\s+month[s]?\s+ago', lambda x: today - timedelta(days=int(x.group(1))*30)),
        # Years ago
        (r'(\d+)\s+year[s]?\s+ago', lambda x: today - timedelta(days=int(x.group(1))*365)),
        # Yesterday
        (r'yesterday', lambda x: today - timedelta(days=1)),
        # Streamed X time ago
        (r'Streamed\s+(\d+)\s+(\w+)\s+ago', lambda x: handle_streamed_time(x)),
        # Specific date
        (r'(\w+\s+\d+,\s+\d{4})', lambda x: datetime.strptime(x.group(1), '%b %d, %Y'))
    ]
    
    for pattern, date_func in patterns:
        match = re.search(pattern, relative_date, re.IGNORECASE)
        if match:
            try:
                date_obj = date_func(match)
                return date_obj.strftime('%Y-%m-%d')
            except Exception as e:
                print(f"Error converting date '{relative_date}': {str(e)}")
                return relative_date
    
    # If no pattern matches, return the original string
    return relative_date

def handle_streamed_time(match):
    """Helper function to handle 'Streamed X time ago' format"""
    amount = int(match.group(1))
    unit = match.group(2).lower()
    today = datetime.now()
    
    if 'hour' in unit:
        return today - timedelta(hours=amount)
    elif 'day' in unit:
        return today - timedelta(days=amount)
    elif 'week' in unit:
        return today - timedelta(weeks=amount)
    elif 'month' in unit:
        return today - timedelta(days=amount*30)
    elif 'year' in unit:
        return today - timedelta(days=amount*365)
    else:
        return today

def find_youtube_links_by_hashtag(hashtag, max_results=10):
    """
    Search YouTube for videos containing the specified hashtag.
    
    Args:
        hashtag (str): The hashtag to search for (without # symbol)
        max_results (int): Maximum number of results to return
        
    Returns:
        list: List of dictionaries containing video information (id, title, publish_time, link)
    """
    search_term = f"#{hashtag}"
    videos_search = VideosSearch(search_term, limit=20)  # Initial limit for each fetch
    
    videos_info = []
    total_videos_found = 0
    previous_count = 0
    no_new_results_count = 0
    max_attempts_without_new = 3  # Exit after this many attempts with no new results
    
    print(f"🔎 Searching for videos with #{hashtag}...")
    
    try:
        while total_videos_found < max_results:
            results = videos_search.result()
            if 'result' in results:
                for video in results['result']:
                    if total_videos_found < max_results:
                        video_id = video.get('id')
                        if video_id:
                            # Extract title and publish time
                            title = video.get('title', 'Unknown Title')
                            relative_publish_time = video.get('publishedTime', 'Unknown Date')
                            
                            # Convert relative date to absolute date
                            absolute_publish_time = convert_relative_to_absolute_date(relative_publish_time)
                            
                            link = f"https://www.youtube.com/watch?v={video_id}"
                            
                            # Check if this link is already in our results
                            if not any(v['link'] == link for v in videos_info):
                                video_data = {
                                    'id': video_id,
                                    'title': title,
                                    'publish_time': absolute_publish_time,
                                    'link': link
                                }
                                videos_info.append(video_data)
                                total_videos_found += 1
                    else:
                        break
            
            # Check if we found any new videos in this batch
            if total_videos_found == previous_count:
                no_new_results_count += 1
                print(f"⚠️ No new results found (attempt {no_new_results_count}/{max_attempts_without_new})")
                if no_new_results_count >= max_attempts_without_new:
                    print(f"🛑 Stopping search after {total_videos_found} results - no more results available")
                    break
            else:
                # Reset counter if we found new videos
                no_new_results_count = 0
            
            # Update previous count
            previous_count = total_videos_found
            
            # If we've already reached the max_results, stop fetching
            if total_videos_found >= max_results:
                print(f"✅ Reached requested limit of {max_results} results")
                break
                
            # Try to fetch the next page of results if we haven't reached the limit
            try:
                videos_search.next()  # Try to fetch the next page of results
                print(f"🔄 Fetching more results... Total videos found: {total_videos_found}")
            except Exception as e:
                print(f"❌ No more results available: {str(e)}")
                break  # Exit the loop if no more results are available
    
    except Exception as e:
        print(f"❌ Error during search: {str(e)}")
    
    print(f"📊 Total videos found for #{hashtag}: {total_videos_found}")
    return videos_info

def save_links_to_csv(videos_info, hashtag, custom_path=None):
    """
    Save the YouTube video information to a CSV file.
    
    Args:
        videos_info (list): List of dictionaries containing video information
        hashtag (str): The hashtag used in the search
        custom_path (str, optional): Custom path to save the file
        
    Returns:
        str: Path to the saved file
    """
    try:
        # Dynamically create a filename based on hashtag
        safe_hashtag = hashtag.replace(' ', '_')
        filename = f"{safe_hashtag}_videos.csv"
        
        if custom_path:
            # Use custom path if provided
            file_path = Path(custom_path)
            if file_path.is_dir():
                # If path is a directory, append the filename
                file_path = file_path / filename
            else:
                # If custom_path includes filename or doesn't exist
                # Make sure parent directory exists
                os.makedirs(file_path.parent, exist_ok=True)
        else:
            # Default to user's documents folder
            documents_path = Path(os.path.expanduser("~")) / "Documents" / "YouTube_Hashtags"
            
            # Create directory if it doesn't exist
            os.makedirs(documents_path, exist_ok=True)
            file_path = documents_path / filename
        
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Updated column headers to include Title and Publication Date
            writer.writerow(["Hashtag", "Title", "Publication Date", "Link"])
            
            # Add video information to each row
            for video in videos_info:
                writer.writerow([
                    f"#{hashtag}",
                    video['title'],
                    video['publish_time'],
                    video['link']
                ])
        
        print(f"\n✅ Saved {len(videos_info)} videos to {file_path}\n")
        print("📝 Tip: When opening in Excel, select all columns and use Format > Column > AutoFit Selection to adjust column widths")
        return str(file_path)
    
    except Exception as e:
        print(f"❌ Error saving file: {str(e)}")
        return None

def open_links_in_browser(videos_info, max_tabs=5):
    """
    Open YouTube links in browser tabs.
    
    Args:
        videos_info (list): List of dictionaries containing video information
        max_tabs (int): Maximum number of tabs to open at once
    """
    if not videos_info:
        print("No links to open.")
        return
    
    try:
        links = [video['link'] for video in videos_info]
        
        # Limit the number of links to max_tabs
        links_to_open = links[:max_tabs]
        
        if len(links) > max_tabs:
            print(f"⚠️ Opening first {max_tabs} of {len(links)} links")
            confirm = input(f"Do you want to open {len(links_to_open)} tabs? (y/n): ").strip().lower()
            if not confirm.startswith('y'):
                print("Operation cancelled.")
                return
        
        for link in links_to_open:
            webbrowser.open_new_tab(link)
        print(f"🚀 Opened {len(links_to_open)} videos in browser tabs")
    
    except Exception as e:
        print(f"❌ Error opening links: {str(e)}")

def process_hashtags(hashtags, max_results, custom_path=None):
    """
    Process multiple hashtags and save their results to separate CSV files.
    
    Args:
        hashtags (list): List of hashtags to search
        max_results (int): Maximum number of results per hashtag
        custom_path (str, optional): Custom path to save the files
    
    Returns:
        dict: A dictionary mapping hashtags to lists of video information
    """
    results = {}
    
    print(f"\n🔄 Processing {len(hashtags)} hashtags...\n")
    
    for i, hashtag in enumerate(hashtags, 1):
        print(f"\n{'=' * 50}")
        print(f"Processing hashtag {i}/{len(hashtags)}: #{hashtag}")
        print(f"{'=' * 50}\n")
        
        videos_info = find_youtube_links_by_hashtag(hashtag, max_results)
        
        if videos_info:
            results[hashtag] = videos_info
            save_links_to_csv(videos_info, hashtag, custom_path)
        else:
            print(f"❌ No videos found for #{hashtag}")
    
    return results

def validate_path(path_str):
    """
    Validate and normalize a file path.
    
    Args:
        path_str (str): Path string to validate
        
    Returns:
        str or None: Normalized path or None if invalid
    """
    if not path_str:
        return None
        
    try:
        # Convert to Path object to normalize
        path_obj = Path(path_str).expanduser().resolve()
        
        # If parent directory doesn't exist, check if we can create it
        if not path_obj.parent.exists():
            try:
                os.makedirs(path_obj.parent, exist_ok=True)
                print(f"✅ Created directory: {path_obj.parent}")
            except PermissionError:
                print(f"❌ Permission denied to create directory: {path_obj.parent}")
                return None
            except Exception as e:
                print(f"❌ Error creating directory: {str(e)}")
                return None
                
        return str(path_obj)
    except Exception as e:
        print(f"❌ Invalid path: {str(e)}")
        return None

def main():
    """Main function to run the script."""
    print("=" * 50)
    print("YouTube Hashtag Video Search Tool (Improved Version)")
    print("=" * 50)
    
    try:
        # Get hashtags from user
        hashtags_input = input("Enter hashtags to search (separate with commas, no # symbol): ").strip()
        if not hashtags_input:
            print("❌ No hashtags entered. Exiting.")
            return
        
        # Parse hashtags and clean them
        hashtags = []
        for tag in hashtags_input.split(','):
            tag = tag.strip()
            # Remove # if user accidentally included it
            if tag.startswith('#'):
                tag = tag[1:]
            if tag:
                hashtags.append(tag)
        
        if not hashtags:
            print("❌ No valid hashtags entered. Exiting.")
            return
        
        print(f"✅ Will search for {len(hashtags)} hashtags: {', '.join(['#' + tag for tag in hashtags])}")
        
        # Get max results per hashtag
        max_results_input = input("How many videos would you like to fetch per hashtag? (default 10): ").strip().lower()
        max_results_input = max_results_input.strip("'\"")  # Remove any accidental quotes
        
        if max_results_input == 'max':
            max_results = sys.maxsize  # Set to system's maximum integer value
            print(f"⚠️ Searching for maximum available results (this might take a while)")
        elif max_results_input:
            try:
                max_results = int(max_results_input)
                if max_results <= 0:
                    print("❌ Number must be positive. Using default of 10.")
                    max_results = 10
                elif max_results > 100:
                    print("⚠️ Large number requested. Limiting to 100 to prevent excessive API usage.")
                    max_results = 100
            except ValueError:
                print("❌ Invalid number entered. Using default of 10.")
                max_results = 10
        else:
            max_results = 10
        
        # Get custom save path (optional)
        custom_path_prompt = input("Enter a custom save location (or press Enter for default Documents/YouTube_Hashtags): ").strip()
        custom_path = validate_path(custom_path_prompt) if custom_path_prompt else None
        
        # Process all hashtags
        all_results = process_hashtags(hashtags, max_results, custom_path)
        
        # Ask if user wants to open links in browser
        if any(all_results.values()):
            total_videos = sum(len(videos) for videos in all_results.values())
            print(f"\n✅ Total videos found across all hashtags: {total_videos}")
            
            open_links_prompt = input("Do you want to open any of these links in your browser? (y/n): ").strip().lower()
            if open_links_prompt.startswith('y'):
                # Which hashtag's links to open
                if len(all_results) > 1:
                    print("\nWhich hashtag's links would you like to open?")
                    for i, tag in enumerate(all_results.keys(), 1):
                        print(f"{i}. #{tag} ({len(all_results[tag])} links)")
                    print(f"{len(all_results) + 1}. All hashtags")
                    
                    choice = input(f"Enter your choice (1-{len(all_results) + 1}): ").strip()
                    try:
                        choice_num = int(choice)
                        if 1 <= choice_num <= len(all_results):
                            # Open links for a single hashtag
                            selected_hashtag = list(all_results.keys())[choice_num - 1]
                            selected_videos = all_results[selected_hashtag]
                            
                            max_tabs_input = input(f"Maximum number of tabs to open for #{selected_hashtag} (default 5): ").strip()
                            try:
                                max_tabs = int(max_tabs_input) if max_tabs_input else 5
                                if max_tabs <= 0:
                                    print("❌ Number must be positive. Using default of 5.")
                                    max_tabs = 5
                            except ValueError:
                                max_tabs = 5
                            
                            open_links_in_browser(selected_videos, max_tabs)
                        elif choice_num == len(all_results) + 1:
                            # Open links for all hashtags
                            all_videos = []
                            for videos in all_results.values():
                                all_videos.extend(videos)
                            
                            max_tabs_input = input(f"Maximum number of tabs to open (default 5, total links: {len(all_videos)}): ").strip()
                            try:
                                max_tabs = int(max_tabs_input) if max_tabs_input else 5
                                if max_tabs <= 0:
                                    print("❌ Number must be positive. Using default of 5.")
                                    max_tabs = 5
                            except ValueError:
                                max_tabs = 5
                            
                            open_links_in_browser(all_videos, max_tabs)
                        else:
                            print("Invalid choice. Not opening any links.")
                    except ValueError:
                        print("Invalid input. Not opening any links.")
                else:
                    # Only one hashtag, open its links
                    only_hashtag = list(all_results.keys())[0]
                    max_tabs_input = input(f"Maximum number of tabs to open for #{only_hashtag} (default 5): ").strip()
                    try:
                        max_tabs = int(max_tabs_input) if max_tabs_input else 5
                        if max_tabs <= 0:
                            print("❌ Number must be positive. Using default of 5.")
                            max_tabs = 5
                    except ValueError:
                        max_tabs = 5
                    
                    open_links_in_browser(all_results[only_hashtag], max_tabs)
        else:
            print("❌ No videos found for any of the hashtags.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")
    finally:
        print("\n" + "=" * 50)
        print("Search complete. Thank you for using YouTube Hashtag Search Tool!")
        print("=" * 50)

if __name__ == "__main__":
    main()