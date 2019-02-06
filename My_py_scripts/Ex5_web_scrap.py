# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 23:15:30 2019

@author: PMuhuri
"""
#Ex5_web_scrap.py
# https://www.digitalocean.com/community/tutorials/how-to-scrape-web-pages-with-beautiful-soup-and-python-3
import requests
from bs4 import BeautifulSoup


page = requests.get('https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ1.htm')

soup = BeautifulSoup(page.text, 'html.parser')

last_links = soup.find(class_='AlphaNav')
last_links.decompose()

artist_name_list = soup.find(class_='BodyText')
artist_name_list_items = artist_name_list.find_all('a')

# Use .contents to pull out the <a> tag’s children
for artist_name in artist_name_list_items:
    names = artist_name.contents[0]
    print(names)