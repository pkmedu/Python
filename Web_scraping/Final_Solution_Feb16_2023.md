```python
# Import required Python libraries

import requests
from bs4 import BeautifulSoup, re, Comment
import pandas as pd  
import xlsxwriter

# Step 1: Scraping the primary "MEPS data file website", 
# finding the data file names that are within the "option"  
# comment tags, and saving them in a csv file

def extractOptions(inputData):
    sub1 = str(re.escape('<option value="All">All data files</option>'))
    sub2 = str(re.escape('</select>'))
    result = re.findall(sub1+"(.*)"+sub2, inputData, flags=re.S)
    if len(result) > 0:
        return result[0]

def extractData(inputData):
    sub1 = str(re.escape('>'))
    sub2 = str(re.escape('</option>'))
    result =  re.findall(sub1+"(.*)"+sub2, inputData, flags=re.S)
    if len(result) > 0:
        return result[0]
    return ''

def main(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        if '<select id="pufnumber" size=1 name="cboPufNumber">' in c:
            #print(c.option.text)
            options = extractOptions(c)
            ops = options.splitlines() #split text into lines
            
            fp = open(r'C:\Data\MEPS_fn.txt', 'w')
            filtered = []
            unwanteds = ['-IC', 'replaced', 'CD-ROM']
            for op in ops:
                data = extractData(op)
                if data.startswith(('MEPS HC', 'HC')) and \
                not any(item in data for item in unwanteds):
                    fp.write(data +'\n') 
                    filtered.append(data)
            fp.close()       
            print(len(filtered), 'public use file names listed on the MEPS website')                       
main('https://meps.ahrq.gov/data_stats/download_data_files.jsp')
```


```python
# Step 2: Creating a Python Pandas DataFrame based on the .txt file created in the previous step
colname=['fn']
df1 = pd.read_csv(r'C:/Data/MEPS_fn.txt',  sep='\t', names = colname)

# Construct the data file URL (domain + query format)
df1['url1'] = "https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-" \
+ df1['fn'].str.extract(r"(\d+[A-Z]*)").sum(axis=1).astype(str)

#  Drop the the column named fn
df1 = df1.drop(columns=['fn'])

print('There are', len(df1), 'MEPS public-use filenames listed in the MEPS Data File Web Page.\n')

# Set the maximum column width
pd.set_option('display.max_colwidth', None)
df1.head()
```


```python
#Step 3: Scraping the MEPS websites and displaying the manipulated data 
pd.set_option("max_colwidth", None)
url2_str_list = []
for item in df1.index:
    url1_str = df1['url1'][item]
    response = requests.get(url1_str)
    soup = BeautifulSoup(response.text, "html.parser")
    li = soup.find(class_ = "OrangeBox").text
    print('URL for', li)  
    print(url1_str)
    print('URLs for the data file in multiple formats, if available')
    for link in soup.find_all('a'):
        if link.text.endswith('ZIP'):
            url2_str = 'https://meps.ahrq.gov' + link.get('href').strip('..')
            print(url2_str)
            url2_str_list.append(url2_str)
print('A total of', f"{len(url2_str_list):,d}", ' MEPS-HC data file format-specific URLs listed on the MEPS website') 
  
```


```python
!jupyter nbconvert --to markdown Final_Solution_Feb16_2023.ipynb
```
