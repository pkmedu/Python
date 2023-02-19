1  #!/usr/bin/env python
2  # coding: utf-8
3  
4  # In[37]:
5  
6  
7  # Import required Python libraries
8  
9  import requests
10  from bs4 import BeautifulSoup, re, Comment
11  import pandas as pd  
12  
13  
14  # Step 1: Create a .txt file by scraping the the MEPS website's option tags' commented data
15  
16  def extractOptions(inputData):
17      sub1 = str(re.escape('<option value="All">All data files</option>'))
18      sub2 = str(re.escape('</select>'))
19      result = re.findall(sub1+"(.*)"+sub2, inputData, flags=re.S)
20      if len(result) > 0:
21          return result[0]
22  
23  def extractData(inputData):
24      sub1 = str(re.escape('>'))
25      sub2 = str(re.escape('</option>'))
26      result =  re.findall(sub1+"(.*)"+sub2, inputData, flags=re.S)
27      if len(result) > 0:
28          return result[0]
29      return ''
30  
31  def main(base_url):
32      response = requests.get(base_url)
33      soup = BeautifulSoup(response.text, "html.parser")
34      comments = soup.find_all(string=lambda text: isinstance(text, Comment))
35      for c in comments:
36          if '<select id="pufnumber" size=1 name="cboPufNumber">' in c:
37              #print(c.option.text)
38              options = extractOptions(c)
39              ops = options.splitlines() #split text into lines
40              
41              fp = open(r'C:\Data\MEPS_fn.txt', 'w')
42              filtered = []
43              unwanteds = ['-IC', 'replaced', 'CD-ROM']
44              for op in ops:
45                  data = extractData(op)
46                  if data.startswith(('MEPS HC', 'HC')) and not any(item in data for item in unwanteds):
47                      fp.write(data +'\n') 
48                      filtered.append(data)
49              fp.close()   
50              print(len(filtered), 'public use file names and description from the MEPS website')    
51              print ()
52              # open, read , and print 5 lines from the file
53              print ('Five file names/description below (out of 402) from the .txt file created from the HTML data')
54              print ()
55              file = open(r'C:\Data\MEPS_fn.txt')
56              content = file.readlines()
57              for item in content[:5]:   print(item)
58  
59  main('https://meps.ahrq.gov/data_stats/download_data_files.jsp')
60      
61  
62  
63  # In[38]:
64  
65  
66  # Step 2: Constrct the the data file URL from the .txt file created in the previous step
67  colname=['fn']
68  df1 = pd.read_csv(r'C:/Data/MEPS_fn.txt',  sep='\t', names = colname)
69  
70  # Construct the data file URL (domain + query format)
71  df1['url1'] = "https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-" + df1['fn'].str.extract(r"(\d+[A-Z]*)").sum(axis=1).astype(str)
72  
73  #  Drop the the column named fn
74  df1 = df1.drop(columns=['fn'])
75  
76  print('There are', len(df1), 'MEPS public-use filenames listed in the MEPS Data File Web Page.')
77  print()
78  list = df1.values.tolist()
79  
80  print('Five sample data file URLs (out of 402) constrcuted from the HTML data')
81  for item in list[:4]:   print(item)
82  
83  
84  # In[ ]:
85  
86  
87  #Step 3: Create data file format-specific URLs from the websites' HTML data for each of the data  files
88  pd.set_option("max_colwidth", None)
89  with open(r'C:\Data\urls.markdown', 'w') as f:
90      url2_str_list = []
91      for item in df1.index:
92          url1_str = df1['url1'][item]
93          response = requests.get(url1_str)
94          soup = BeautifulSoup(response.text, "html.parser")
95          li = soup.find(class_ = "OrangeBox").text
96          print('URL for', li, file = f)  
97          print(url1_str, file = f)
98          print('URLs for the data file in multiple formats, if available',file = f)
99          for link in soup.find_all('a'):
100              if link.text.endswith('ZIP'):
101                  url2_str = 'https://meps.ahrq.gov' + link.get('href').strip('..')
102                  print(url2_str, file = f)       
103                  url2_str_list.append(url2_str)
104                                  
105  print('A total of', f"{len(url2_str_list):,d}", ' MEPS-HC data file format-specific URLs listed on the MEPS website') 
106  print()
107  print ('Below is a small portion of the bulk output saved in a file.')
108  print("(Sample MEPS data file-URL along its five data format-specific URLs - out of 1,154 URLs)")
109  print()   
110  file = open(r'C:\Data\urls.markdown')
111  content = file.readlines()
112  for item in content[:8]:     print(item)
113  
114  
115  # In[ ]:
116  
117  
118  get_ipython().system('jupyter nbconvert --to markdown Final_Solution_Feb18_2023.ipynb')
119  
120  
121  # In[36]:
122  
123  
124  get_ipython().system('jupyter nbconvert --to python Final_Solution_Feb18_2023.ipynb')
125  
126  
127  # In[ ]:
128  
129  
130  
131  
