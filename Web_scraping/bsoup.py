# Step 1: List all MEPS data file URLs 
%%writefile bsoup.py
import requests
from bs4 import BeautifulSoup

full_url_list = []
tuple_values = 'v9.zip', 'ssp.zip', 'dta.zip', 'dat.zip', 'xlsx.zip', '/'
def get_links(base_url):
    response = requests.get(base_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all('a')
    for tag in tags:
        if tag.text.endswith(tuple_values):
            href = tag.get_text()
            full_url = base_url + href
            if href[-1]=='/':
                get_links(full_url)        
            else:
                #print(full_url)
                full_url_list.append(full_url)
                
get_links('https://meps.ahrq.gov/data_files/pufs/')
print('There are', f"{len(full_url_list):,}", 'Full URLs for 5 format-specific data files.')

print('Listing of first 5 URLs')
for item in full_url_list[:5]:   print(item)
