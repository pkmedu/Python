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
            options = extractOptions(c)
            ops = options.splitlines() #split text into lines
            fp = open(r'C:/Data/MEPS_fn.csv', 'w')
            for op in ops:
                data = extractData(op)
                if data.startswith(("MEPS HC", "HC")):
                    if "-IC" not in data:
                        if "replaced" not in data:  
                            if "CD-ROM" not in data:
                                #print(data)
                                fp.write(data +'\n')                    
            fp.close()    
            
            with open(r'C:\Data\MEPS_fn.csv', 'r') as buff:
                for i, line in enumerate(buff, 1):
                    pass
                print(f"{(i)}", 'file names listed in the MEPS website') 
                
main('https://meps.ahrq.gov/data_stats/download_data_files.jsp')
```

    402 file names listed in the MEPS website
    


```python
# Step 2: Creating a Python Pandas DataFrame based on the .csv file created in the previous step

colname = ['file_name']
df1 = pd.read_csv(r'C:/Data/MEPS_fn.csv',  sep='\t', names = colname)

df1["url1"] = "https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-" \
+ df1["file_name"].str.extract(r"(\d+[A-Z]*)").sum(axis=1).astype(str)

df1.reset_index(drop = True, inplace = True)

print('There are', f"{len(df1)}", 'MEPS public-use filenames listed in the MEPS Data File Web Page.\n')

```

    There are 402 MEPS public-use filenames listed in the MEPS Data File Web Page.
    
    


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

    URL for MEPS HC-226: MEPS Panel 23 Three-Year Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-226
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h226/h226dat.zip
    https://meps.ahrq.gov/data_files/pufs/h226/h226ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h226/h226v9.zip
    https://meps.ahrq.gov/data_files/pufs/h226/h226dta.zip
    https://meps.ahrq.gov/data_files/pufs/h226/h226xlsx.zip
    URL for MEPS HC-225: MEPS Panel 24 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-225
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h225/h225dat.zip
    https://meps.ahrq.gov/data_files/pufs/h225/h225ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h225/h225v9.zip
    https://meps.ahrq.gov/data_files/pufs/h225/h225dta.zip
    https://meps.ahrq.gov/data_files/pufs/h225/h225xlsx.zip
    URL for MEPS HC-224: 2020 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-224
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h224/h224dat.zip
    https://meps.ahrq.gov/data_files/pufs/h224/h224ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h224/h224v9.zip
    https://meps.ahrq.gov/data_files/pufs/h224/h224dta.zip
    https://meps.ahrq.gov/data_files/pufs/h224/h224xlsx.zip
    URL for MEPS HC-223: 2020 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-223
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h223/h223dat.zip
    https://meps.ahrq.gov/data_files/pufs/h223/h223ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h223/h223v9.zip
    https://meps.ahrq.gov/data_files/pufs/h223/h223dta.zip
    https://meps.ahrq.gov/data_files/pufs/h223/h223xlsx.zip
    URL for MEPS HC-222: 2020 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-222
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h222/h222dat.zip
    https://meps.ahrq.gov/data_files/pufs/h222/h222ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h222/h222v9.zip
    https://meps.ahrq.gov/data_files/pufs/h222/h222dta.zip
    https://meps.ahrq.gov/data_files/pufs/h222/h222xlsx.zip
    URL for MEPS HC-221: 2020 Food Security File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-221
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h221/h221dat.zip
    https://meps.ahrq.gov/data_files/pufs/h221/h221ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h221/h221v9.zip
    https://meps.ahrq.gov/data_files/pufs/h221/h221dta.zip
    https://meps.ahrq.gov/data_files/pufs/h221/h221xlsx.zip
    URL for MEPS HC-220I: Appendix to MEPS 2020 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-220I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h220i/h220if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h220i/h220if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h220i/h220if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h220i/h220if2ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h220i/h220if1v9.zip
    https://meps.ahrq.gov/data_files/pufs/h220i/h220if2v9.zip
    https://meps.ahrq.gov/data_files/pufs/h220i/h220if1dta.zip
    https://meps.ahrq.gov/data_files/pufs/h220i/h220if2dta.zip
    https://meps.ahrq.gov/data_files/pufs/h220i/h220if1xlsx.zip
    https://meps.ahrq.gov/data_files/pufs/h220i/h220if2xlsx.zip
    URL for MEPS HC-220H: 2020 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-220H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h220h/h220hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h220h/h220hssp.zip
    https://meps.ahrq.gov/data_files/pufs/h220h/h220hv9.zip
    https://meps.ahrq.gov/data_files/pufs/h220h/h220hdta.zip
    https://meps.ahrq.gov/data_files/pufs/h220h/h220hxlsx.zip
    URL for MEPS HC-220G: 2020 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-220G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h220g/h220gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h220g/h220gssp.zip
    https://meps.ahrq.gov/data_files/pufs/h220g/h220gv9.zip
    https://meps.ahrq.gov/data_files/pufs/h220g/h220gdta.zip
    https://meps.ahrq.gov/data_files/pufs/h220g/h220gxlsx.zip
    URL for MEPS HC-220F: 2020 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-220F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h220f/h220fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h220f/h220fssp.zip
    https://meps.ahrq.gov/data_files/pufs/h220f/h220fv9.zip
    https://meps.ahrq.gov/data_files/pufs/h220f/h220fdta.zip
    https://meps.ahrq.gov/data_files/pufs/h220f/h220fxlsx.zip
    URL for MEPS HC-220E: 2020 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-220E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h220e/h220edat.zip
    https://meps.ahrq.gov/data_files/pufs/h220e/h220essp.zip
    https://meps.ahrq.gov/data_files/pufs/h220e/h220ev9.zip
    https://meps.ahrq.gov/data_files/pufs/h220e/h220edta.zip
    https://meps.ahrq.gov/data_files/pufs/h220e/h220exlsx.zip
    URL for MEPS HC-220D: 2020 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-220D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h220d/h220ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h220d/h220dssp.zip
    https://meps.ahrq.gov/data_files/pufs/h220d/h220dv9.zip
    https://meps.ahrq.gov/data_files/pufs/h220d/h220ddta.zip
    https://meps.ahrq.gov/data_files/pufs/h220d/h220dxlsx.zip
    URL for MEPS HC-220C: 2020 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-220C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h220c/h220cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h220c/h220cssp.zip
    https://meps.ahrq.gov/data_files/pufs/h220c/h220cv9.zip
    https://meps.ahrq.gov/data_files/pufs/h220c/h220cdta.zip
    https://meps.ahrq.gov/data_files/pufs/h220c/h220cxlsx.zip
    URL for MEPS HC-220B: 2020 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-220B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h220b/h220bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h220b/h220bssp.zip
    https://meps.ahrq.gov/data_files/pufs/h220b/h220bv9.zip
    https://meps.ahrq.gov/data_files/pufs/h220b/h220bdta.zip
    https://meps.ahrq.gov/data_files/pufs/h220b/h220bxlsx.zip
    URL for MEPS HC-220A: 2020 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-220A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h220a/h220adat.zip
    https://meps.ahrq.gov/data_files/pufs/h220a/h220assp.zip
    https://meps.ahrq.gov/data_files/pufs/h220a/h220av9.zip
    https://meps.ahrq.gov/data_files/pufs/h220a/h220adta.zip
    https://meps.ahrq.gov/data_files/pufs/h220a/h220axlsx.zip
    URL for MEPS HC-219: 2020 Full Year Population Characteristics File(HC-219 replaced by HC-224)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-219
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h219/h219dat.zip
    https://meps.ahrq.gov/data_files/pufs/h219/h219ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h219/h219v9.zip
    https://meps.ahrq.gov/data_files/pufs/h219/h219dta.zip
    https://meps.ahrq.gov/data_files/pufs/h219/h219xlsx.zip
    URL for MEPS HC-218: 2020 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-218
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h218/h218dat.zip
    https://meps.ahrq.gov/data_files/pufs/h218/h218ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h218/h218v9.zip
    https://meps.ahrq.gov/data_files/pufs/h218/h218dta.zip
    https://meps.ahrq.gov/data_files/pufs/h218/h218xlsx.zip
    URL for MEPS HC-217: MEPS Panel 23 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-217
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h217/h217dat.zip
    https://meps.ahrq.gov/data_files/pufs/h217/h217ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h217/h217v9.zip
    https://meps.ahrq.gov/data_files/pufs/h217/h217dta.zip
    https://meps.ahrq.gov/data_files/pufs/h217/h217xlsx.zip
    URL for MEPS HC-216: 2019 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-216
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h216/h216dat.zip
    https://meps.ahrq.gov/data_files/pufs/h216/h216ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h216/h216v9.zip
    https://meps.ahrq.gov/data_files/pufs/h216/h216dta.zip
    https://meps.ahrq.gov/data_files/pufs/h216/h216xlsx.zip
    URL for MEPS HC-215: 2019 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-215
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h215/h215dat.zip
    https://meps.ahrq.gov/data_files/pufs/h215/h215ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h215/h215v9.zip
    https://meps.ahrq.gov/data_files/pufs/h215/h215dta.zip
    https://meps.ahrq.gov/data_files/pufs/h215/h215xlsx.zip
    URL for MEPS HC-214: 2019 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-214
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h214/h214dat.zip
    https://meps.ahrq.gov/data_files/pufs/h214/h214ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h214/h214v9.zip
    https://meps.ahrq.gov/data_files/pufs/h214/h214dta.zip
    https://meps.ahrq.gov/data_files/pufs/h214/h214xlsx.zip
    URL for MEPS HC-213I: Appendix to MEPS 2019 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-213I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h213i/h213if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h213i/h213if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h213i/h213if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h213i/h213if2ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h213i/h213if1v9.zip
    https://meps.ahrq.gov/data_files/pufs/h213i/h213if2v9.zip
    https://meps.ahrq.gov/data_files/pufs/h213i/h213if1dta.zip
    https://meps.ahrq.gov/data_files/pufs/h213i/h213if2dta.zip
    https://meps.ahrq.gov/data_files/pufs/h213i/h213if1xlsx.zip
    https://meps.ahrq.gov/data_files/pufs/h213i/h213if2xlsx.zip
    URL for MEPS HC-213H: 2019 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-213H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h213h/h213hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h213h/h213hssp.zip
    https://meps.ahrq.gov/data_files/pufs/h213h/h213hv9.zip
    https://meps.ahrq.gov/data_files/pufs/h213h/h213hdta.zip
    https://meps.ahrq.gov/data_files/pufs/h213h/h213hxlsx.zip
    URL for MEPS HC-213G: 2019 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-213G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h213g/h213gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h213g/h213gssp.zip
    https://meps.ahrq.gov/data_files/pufs/h213g/h213gv9.zip
    https://meps.ahrq.gov/data_files/pufs/h213g/h213gdta.zip
    https://meps.ahrq.gov/data_files/pufs/h213g/h213gxlsx.zip
    URL for MEPS HC-213F: 2019 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-213F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h213f/h213fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h213f/h213fssp.zip
    https://meps.ahrq.gov/data_files/pufs/h213f/h213fv9.zip
    https://meps.ahrq.gov/data_files/pufs/h213f/h213fdta.zip
    https://meps.ahrq.gov/data_files/pufs/h213f/h213fxlsx.zip
    URL for MEPS HC-213E: 2019 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-213E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h213e/h213edat.zip
    https://meps.ahrq.gov/data_files/pufs/h213e/h213essp.zip
    https://meps.ahrq.gov/data_files/pufs/h213e/h213ev9.zip
    https://meps.ahrq.gov/data_files/pufs/h213e/h213edta.zip
    https://meps.ahrq.gov/data_files/pufs/h213e/h213exlsx.zip
    URL for MEPS HC-213D: 2019 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-213D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h213d/h213ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h213d/h213dssp.zip
    https://meps.ahrq.gov/data_files/pufs/h213d/h213dv9.zip
    https://meps.ahrq.gov/data_files/pufs/h213d/h213ddta.zip
    https://meps.ahrq.gov/data_files/pufs/h213d/h213dxlsx.zip
    URL for MEPS HC-213C: 2019 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-213C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h213c/h213cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h213c/h213cssp.zip
    https://meps.ahrq.gov/data_files/pufs/h213c/h213cv9.zip
    https://meps.ahrq.gov/data_files/pufs/h213c/h213cdta.zip
    https://meps.ahrq.gov/data_files/pufs/h213c/h213cxlsx.zip
    URL for MEPS HC-213B: 2019 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-213B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h213b/h213bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h213b/h213bssp.zip
    https://meps.ahrq.gov/data_files/pufs/h213b/h213bv9.zip
    https://meps.ahrq.gov/data_files/pufs/h213b/h213bdta.zip
    https://meps.ahrq.gov/data_files/pufs/h213b/h213bxlsx.zip
    URL for MEPS HC-213A: 2019 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-213A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h213a/h213adat.zip
    https://meps.ahrq.gov/data_files/pufs/h213a/h213assp.zip
    https://meps.ahrq.gov/data_files/pufs/h213a/h213av9.zip
    https://meps.ahrq.gov/data_files/pufs/h213a/h213adta.zip
    https://meps.ahrq.gov/data_files/pufs/h213a/h213axlsx.zip
    URL for MEPS HC-212: 2019 Full Year Population Characteristics File (HC-212 replaced by HC-216)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-212
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h212/h212dat.zip
    https://meps.ahrq.gov/data_files/pufs/h212/h212ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h212/h212v9.zip
    https://meps.ahrq.gov/data_files/pufs/h212/h212dta.zip
    https://meps.ahrq.gov/data_files/pufs/h212/h212xlsx.zip
    URL for MEPS HC-211: 2019 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-211
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h211/h211dat.zip
    https://meps.ahrq.gov/data_files/pufs/h211/h211ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h211/h211v9.zip
    https://meps.ahrq.gov/data_files/pufs/h211/h211dta.zip
    https://meps.ahrq.gov/data_files/pufs/h211/h211xlsx.zip
    URL for MEPS HC-210: MEPS Panel 22 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-210
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h210/h210dat.zip
    https://meps.ahrq.gov/data_files/pufs/h210/h210ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h210/h210v9.zip
    https://meps.ahrq.gov/data_files/pufs/h210/h210dta.zip
    https://meps.ahrq.gov/data_files/pufs/h210/h210xlsx.zip
    URL for MEPS HC-209: 2018 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-209
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h209/h209dat.zip
    https://meps.ahrq.gov/data_files/pufs/h209/h209ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h209/h209v9.zip
    https://meps.ahrq.gov/data_files/pufs/h209/h209dta.zip
    https://meps.ahrq.gov/data_files/pufs/h209/h209xlsx.zip
    URL for MEPS HC-208: 2018 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-208
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h208/h208dat.zip
    https://meps.ahrq.gov/data_files/pufs/h208/h208ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h208/h208v9.zip
    https://meps.ahrq.gov/data_files/pufs/h208/h208dta.zip
    https://meps.ahrq.gov/data_files/pufs/h208/h208xlsx.zip
    URL for MEPS HC-207: 2018 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-207
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h207/h207dat.zip
    https://meps.ahrq.gov/data_files/pufs/h207/h207ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h207/h207v9.zip
    https://meps.ahrq.gov/data_files/pufs/h207/h207dta.zip
    https://meps.ahrq.gov/data_files/pufs/h207/h207xlsx.zip
    URL for MEPS HC-206I: Appendix to MEPS 2018 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-206I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h206i/h206if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h206i/h206if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h206i/h206if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h206i/h206if2ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h206i/h206if1v9.zip
    https://meps.ahrq.gov/data_files/pufs/h206i/h206if2v9.zip
    https://meps.ahrq.gov/data_files/pufs/h206i/h206if1dta.zip
    https://meps.ahrq.gov/data_files/pufs/h206i/h206if2dta.zip
    https://meps.ahrq.gov/data_files/pufs/h206i/h206if1xlsx.zip
    https://meps.ahrq.gov/data_files/pufs/h206i/h206if2xlsx.zip
    URL for MEPS HC-206H: 2018 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-206H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h206h/h206hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h206h/h206hssp.zip
    https://meps.ahrq.gov/data_files/pufs/h206h/h206hv9.zip
    https://meps.ahrq.gov/data_files/pufs/h206h/h206hdta.zip
    https://meps.ahrq.gov/data_files/pufs/h206h/h206hxlsx.zip
    URL for MEPS HC-206G: 2018 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-206G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h206g/h206gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h206g/h206gssp.zip
    https://meps.ahrq.gov/data_files/pufs/h206g/h206gv9.zip
    https://meps.ahrq.gov/data_files/pufs/h206g/h206gdta.zip
    https://meps.ahrq.gov/data_files/pufs/h206g/h206gxlsx.zip
    URL for MEPS HC-206F: 2018 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-206F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h206f/h206fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h206f/h206fssp.zip
    https://meps.ahrq.gov/data_files/pufs/h206f/h206fv9.zip
    https://meps.ahrq.gov/data_files/pufs/h206f/h206fdta.zip
    https://meps.ahrq.gov/data_files/pufs/h206f/h206fxlsx.zip
    URL for MEPS HC-206E: 2018 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-206E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h206e/h206edat.zip
    https://meps.ahrq.gov/data_files/pufs/h206e/h206essp.zip
    https://meps.ahrq.gov/data_files/pufs/h206e/h206ev9.zip
    https://meps.ahrq.gov/data_files/pufs/h206e/h206edta.zip
    https://meps.ahrq.gov/data_files/pufs/h206e/h206exlsx.zip
    URL for MEPS HC-206D: 2018 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-206D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h206d/h206ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h206d/h206dssp.zip
    https://meps.ahrq.gov/data_files/pufs/h206d/h206dv9.zip
    https://meps.ahrq.gov/data_files/pufs/h206d/h206ddta.zip
    https://meps.ahrq.gov/data_files/pufs/h206d/h206dxlsx.zip
    URL for MEPS HC-206C: 2018 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-206C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h206c/h206cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h206c/h206cssp.zip
    https://meps.ahrq.gov/data_files/pufs/h206c/h206cv9.zip
    https://meps.ahrq.gov/data_files/pufs/h206c/h206cdta.zip
    https://meps.ahrq.gov/data_files/pufs/h206c/h206cxlsx.zip
    URL for MEPS HC-206B: 2018 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-206B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h206b/h206bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h206b/h206bssp.zip
    https://meps.ahrq.gov/data_files/pufs/h206b/h206bv9.zip
    https://meps.ahrq.gov/data_files/pufs/h206b/h206bdta.zip
    https://meps.ahrq.gov/data_files/pufs/h206b/h206bxlsx.zip
    URL for MEPS HC-206A: 2018 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-206A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h206a/h206adat.zip
    https://meps.ahrq.gov/data_files/pufs/h206a/h206assp.zip
    https://meps.ahrq.gov/data_files/pufs/h206a/h206av9.zip
    https://meps.ahrq.gov/data_files/pufs/h206a/h206adta.zip
    https://meps.ahrq.gov/data_files/pufs/h206a/h206axlsx.zip
    URL for MEPS HC-205: 2019 P23R3/P24R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-205
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h205/h205dat.zip
    https://meps.ahrq.gov/data_files/pufs/h205/h205ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h205/h205v9.zip
    https://meps.ahrq.gov/data_files/pufs/h205/h205dta.zip
    https://meps.ahrq.gov/data_files/pufs/h205/h205xlsx.zip
    URL for MEPS HC-204: 2018 Full Year Population Characteristics File (HC-204 replaced by HC-209)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-204
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h204/h204dat.zip
    https://meps.ahrq.gov/data_files/pufs/h204/h204ssp.zip
    URL for MEPS HC-203: 2018 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-203
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h203/h203dat.zip
    https://meps.ahrq.gov/data_files/pufs/h203/h203ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h203/h203v9.zip
    https://meps.ahrq.gov/data_files/pufs/h203/h203dta.zip
    https://meps.ahrq.gov/data_files/pufs/h203/h203xlsx.zip
    URL for MEPS HC-202: MEPS Panel 21 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-202
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h202/h202dat.zip
    https://meps.ahrq.gov/data_files/pufs/h202/h202ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h202/h202v9.zip
    https://meps.ahrq.gov/data_files/pufs/h202/h202dta.zip
    https://meps.ahrq.gov/data_files/pufs/h202/h202xlsx.zip
    URL for MEPS HC-201: 2017 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-201
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h201/h201dat.zip
    https://meps.ahrq.gov/data_files/pufs/h201/h201ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h201/h201v9.zip
    https://meps.ahrq.gov/data_files/pufs/h201/h201dta.zip
    https://meps.ahrq.gov/data_files/pufs/h201/h201xlsx.zip
    URL for MEPS HC-200: 2017 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-200
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h200/h200dat.zip
    https://meps.ahrq.gov/data_files/pufs/h200/h200ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h200/h200v9.zip
    https://meps.ahrq.gov/data_files/pufs/h200/h200dta.zip
    https://meps.ahrq.gov/data_files/pufs/h200/h200xlsx.zip
    URL for MEPS HC-199: 2017 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-199
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h199/h199dat.zip
    https://meps.ahrq.gov/data_files/pufs/h199/h199ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h199/h199v9.zip
    https://meps.ahrq.gov/data_files/pufs/h199/h199dta.zip
    https://meps.ahrq.gov/data_files/pufs/h199/h199xlsx.zip
    URL for MEPS HC-198: 2017 Food Security File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-198
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h198/h198dat.zip
    https://meps.ahrq.gov/data_files/pufs/h198/h198ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h198/h198v9.zip
    https://meps.ahrq.gov/data_files/pufs/h198/h198dta.zip
    https://meps.ahrq.gov/data_files/pufs/h198/h198xlsx.zip
    URL for MEPS HC-197I: Appendix to MEPS 2017 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-197I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h197i/h197if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h197i/h197if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h197i/h197if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h197i/h197if2ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h197i/h197if1v9.zip
    https://meps.ahrq.gov/data_files/pufs/h197i/h197if2v9.zip
    https://meps.ahrq.gov/data_files/pufs/h197i/h197if1dta.zip
    https://meps.ahrq.gov/data_files/pufs/h197i/h197if2dta.zip
    https://meps.ahrq.gov/data_files/pufs/h197i/h197if1xlsx.zip
    https://meps.ahrq.gov/data_files/pufs/h197i/h197if2xlsx.zip
    URL for MEPS HC-197H: 2017 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-197H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h197h/h197hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h197h/h197hssp.zip
    https://meps.ahrq.gov/data_files/pufs/h197h/h197hv9.zip
    https://meps.ahrq.gov/data_files/pufs/h197h/h197hdta.zip
    https://meps.ahrq.gov/data_files/pufs/h197h/h197hxlsx.zip
    URL for MEPS HC-197G: 2017 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-197G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h197g/h197gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h197g/h197gssp.zip
    https://meps.ahrq.gov/data_files/pufs/h197g/h197gv9.zip
    https://meps.ahrq.gov/data_files/pufs/h197g/h197gdta.zip
    https://meps.ahrq.gov/data_files/pufs/h197g/h197gxlsx.zip
    URL for MEPS HC-197F: 2017 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-197F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h197f/h197fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h197f/h197fssp.zip
    https://meps.ahrq.gov/data_files/pufs/h197f/h197fv9.zip
    https://meps.ahrq.gov/data_files/pufs/h197f/h197fdta.zip
    https://meps.ahrq.gov/data_files/pufs/h197f/h197fxlsx.zip
    URL for MEPS HC-197E: 2017 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-197E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h197e/h197edat.zip
    https://meps.ahrq.gov/data_files/pufs/h197e/h197essp.zip
    https://meps.ahrq.gov/data_files/pufs/h197e/h197ev9.zip
    https://meps.ahrq.gov/data_files/pufs/h197e/h197edta.zip
    https://meps.ahrq.gov/data_files/pufs/h197e/h197exlsx.zip
    URL for MEPS HC-197D: 2017 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-197D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h197d/h197ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h197d/h197dssp.zip
    https://meps.ahrq.gov/data_files/pufs/h197d/h197dv9.zip
    https://meps.ahrq.gov/data_files/pufs/h197d/h197ddta.zip
    https://meps.ahrq.gov/data_files/pufs/h197d/h197dxlsx.zip
    URL for MEPS HC-197C: 2017 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-197C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h197c/h197cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h197c/h197cssp.zip
    https://meps.ahrq.gov/data_files/pufs/h197c/h197cv9.zip
    https://meps.ahrq.gov/data_files/pufs/h197c/h197cdta.zip
    https://meps.ahrq.gov/data_files/pufs/h197c/h197cxlsx.zip
    URL for MEPS HC-197B: 2017 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-197B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h197b/h197bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h197b/h197bssp.zip
    https://meps.ahrq.gov/data_files/pufs/h197b/h197bv9.zip
    https://meps.ahrq.gov/data_files/pufs/h197b/h197bdta.zip
    https://meps.ahrq.gov/data_files/pufs/h197b/h197bxlsx.zip
    URL for MEPS HC-197A: 2017 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-197A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h197a/h197adat.zip
    https://meps.ahrq.gov/data_files/pufs/h197a/h197assp.zip
    https://meps.ahrq.gov/data_files/pufs/h197a/h197av9.zip
    https://meps.ahrq.gov/data_files/pufs/h197a/h197adta.zip
    https://meps.ahrq.gov/data_files/pufs/h197a/h197axlsx.zip
    URL for MEPS HC-196: 2018 P22R3/P23R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-196
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h196/h196dat.zip
    https://meps.ahrq.gov/data_files/pufs/h196/h196ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h196/h196v9.zip
    https://meps.ahrq.gov/data_files/pufs/h196/h196dta.zip
    https://meps.ahrq.gov/data_files/pufs/h196/h196xlsx.zip
    URL for MEPS HC-195: 2017 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-195
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h195/h195dat.zip
    https://meps.ahrq.gov/data_files/pufs/h195/h195ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h195/h195v9.zip
    https://meps.ahrq.gov/data_files/pufs/h195/h195dta.zip
    https://meps.ahrq.gov/data_files/pufs/h195/h195xlsx.zip
    URL for MEPS HC-194: 2017 Full Year Population Characteristics File (HC-194 replaced by HC-201)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-194
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h194dat.zip
    https://meps.ahrq.gov/data_files/pufs/h194ssp.zip
    URL for MEPS HC-193: MEPS Panel 20 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-193
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h193dat.zip
    https://meps.ahrq.gov/data_files/pufs/h193ssp.zip
    URL for MEPS HC-192: 2016 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-192
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h192dat.zip
    https://meps.ahrq.gov/data_files/pufs/h192ssp.zip
    URL for MEPS HC-191: 2016 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-191
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h191dat.zip
    https://meps.ahrq.gov/data_files/pufs/h191ssp.zip
    URL for MEPS HC-190: 2016 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-190
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h190/h190dat.zip
    https://meps.ahrq.gov/data_files/pufs/h190/h190ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h190/h190v9.zip
    https://meps.ahrq.gov/data_files/pufs/h190/h190dta.zip
    https://meps.ahrq.gov/data_files/pufs/h190/h190xlsx.zip
    URL for MEPS HC-189: 2016 Food Security File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-189
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h189dat.zip
    https://meps.ahrq.gov/data_files/pufs/h189ssp.zip
    URL for MEPS HC-188I: Appendix to MEPS 2016 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-188I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h188if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h188if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h188if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h188if2ssp.zip
    URL for MEPS HC-188H: 2016 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-188H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h188hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h188hssp.zip
    URL for MEPS HC-188G: 2016 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-188G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h188gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h188gssp.zip
    URL for MEPS HC-188F: 2016 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-188F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h188fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h188fssp.zip
    URL for MEPS HC-188E: 2016 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-188E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h188edat.zip
    https://meps.ahrq.gov/data_files/pufs/h188essp.zip
    URL for MEPS HC-188D: 2016 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-188D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h188ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h188dssp.zip
    URL for MEPS HC-188C: 2016 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-188C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h188cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h188cssp.zip
    URL for MEPS HC-188B: 2016 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-188B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h188bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h188bssp.zip
    URL for MEPS HC-188A: 2016 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-188A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h188adat.zip
    https://meps.ahrq.gov/data_files/pufs/h188assp.zip
    URL for MEPS HC-187: 2016 Full Year Medical Organizations Survey File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-187
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h187dat.zip
    https://meps.ahrq.gov/data_files/pufs/h187ssp.zip
    URL for MEPS HC-186: 2017 P21R3/P22R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-186
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h186/h186dat.zip
    https://meps.ahrq.gov/data_files/pufs/h186/h186ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h186/h186v9.zip
    https://meps.ahrq.gov/data_files/pufs/h186/h186dta.zip
    https://meps.ahrq.gov/data_files/pufs/h186/h186xlsx.zip
    URL for MEPS HC-185: 2016 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-185
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h185dat.zip
    https://meps.ahrq.gov/data_files/pufs/h185ssp.zip
    URL for MEPS HC-184: 2016 Full Year Population Characteristics File (HC-184 replaced by HC-192)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-184
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h184dat.zip
    https://meps.ahrq.gov/data_files/pufs/h184ssp.zip
    URL for MEPS HC-183: MEPS Panel 19 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-183
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h183dat.zip
    https://meps.ahrq.gov/data_files/pufs/h183ssp.zip
    URL for MEPS HC-182: 2015 Full Year Medical Organizations Survey File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-182
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h182dat.zip
    https://meps.ahrq.gov/data_files/pufs/h182ssp.zip
    URL for MEPS HC-181: 2015 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-181
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h181dat.zip
    https://meps.ahrq.gov/data_files/pufs/h181ssp.zip
    URL for MEPS HC-180: 2015 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-180
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h180dat.zip
    https://meps.ahrq.gov/data_files/pufs/h180ssp.zip
    URL for MEPS HC-179: 2015 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-179
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h179dat.zip
    https://meps.ahrq.gov/data_files/pufs/h179ssp.zip
    URL for MEPS HC-178I: Appendix to MEPS 2015 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-178I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h178if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h178if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h178if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h178if2ssp.zip
    URL for MEPS HC-178H: 2015 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-178H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h178hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h178hssp.zip
    URL for MEPS HC-178G: 2015 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-178G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h178gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h178gssp.zip
    URL for MEPS HC-178F: 2015 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-178F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h178fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h178fssp.zip
    URL for MEPS HC-178E: 2015 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-178E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h178edat.zip
    https://meps.ahrq.gov/data_files/pufs/h178essp.zip
    URL for MEPS HC-178D: 2015 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-178D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h178ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h178dssp.zip
    URL for MEPS HC-178C: 2015 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-178C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h178cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h178cssp.zip
    URL for MEPS HC-178B: 2015 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-178B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h178bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h178bssp.zip
    URL for MEPS HC-178A: 2015 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-178A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h178adat.zip
    https://meps.ahrq.gov/data_files/pufs/h178assp.zip
    URL for MEPS HC-177: 2016 P20R3/P21R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-177
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h177dat.zip
    https://meps.ahrq.gov/data_files/pufs/h177ssp.zip
    URL for MEPS HC-176: 2015 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-176
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h176dat.zip
    https://meps.ahrq.gov/data_files/pufs/h176ssp.zip
    URL for MEPS HC-174: 2015 Full Year Population Characteristics (HC-174 replaced by HC-181)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-174
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h174dat.zip
    https://meps.ahrq.gov/data_files/pufs/h174ssp.zip
    URL for MEPS HC-173: 2014 Preventive Care Self-Administered Questionnaire File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-173
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h173dat.zip
    https://meps.ahrq.gov/data_files/pufs/h173ssp.zip
    URL for MEPS HC-172: MEPS Panel 18 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-172
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h172dat.zip
    https://meps.ahrq.gov/data_files/pufs/h172ssp.zip
    URL for MEPS HC-171: 2014 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-171
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h171dat.zip
    https://meps.ahrq.gov/data_files/pufs/h171ssp.zip
    URL for MEPS HC-170: 2014 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-170
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h170dat.zip
    https://meps.ahrq.gov/data_files/pufs/h170ssp.zip
    URL for MEPS HC-169: 2014 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-169
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h169dat.zip
    https://meps.ahrq.gov/data_files/pufs/h169ssp.zip
    URL for MEPS HC-168I: Appendix to MEPS 2014 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-168I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h168if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h168if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h168if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h168if2ssp.zip
    URL for MEPS HC-168H: 2014 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-168H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h168hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h168hssp.zip
    URL for MEPS HC-168G: 2014 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-168G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h168gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h168gssp.zip
    URL for MEPS HC-168F: 2014 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-168F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h168fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h168fssp.zip
    URL for MEPS HC-168E: 2014 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-168E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h168edat.zip
    https://meps.ahrq.gov/data_files/pufs/h168essp.zip
    URL for MEPS HC-168D: 2014 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-168D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h168ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h168dssp.zip
    URL for MEPS HC-168C: 2014 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-168C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h168cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h168cssp.zip
    URL for MEPS HC-168B: 2014 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-168B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h168bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h168bssp.zip
    URL for MEPS HC-168A: 2014 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-168A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h168adat.zip
    https://meps.ahrq.gov/data_files/pufs/h168assp.zip
    URL for MEPS HC-167: 2015 P19R3/P20R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-167
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h167dat.zip
    https://meps.ahrq.gov/data_files/pufs/h167ssp.zip
    URL for MEPS HC-166: 2014 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-166
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h166dat.zip
    https://meps.ahrq.gov/data_files/pufs/h166ssp.zip
    URL for MEPS HC-165: 2014 Full Year Population Characteristics (HC-165 replaced by HC-171)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-165
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h165dat.zip
    https://meps.ahrq.gov/data_files/pufs/h165ssp.zip
    URL for MEPS HC-164: MEPS Panel 17 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-164
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h164dat.zip
    https://meps.ahrq.gov/data_files/pufs/h164ssp.zip
    URL for MEPS HC-163: 2013 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-163
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h163dat.zip
    https://meps.ahrq.gov/data_files/pufs/h163ssp.zip
    URL for MEPS HC-162: 2013 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-162
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h162dat.zip
    https://meps.ahrq.gov/data_files/pufs/h162ssp.zip
    URL for MEPS HC-161: 2013 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-161
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h161dat.zip
    https://meps.ahrq.gov/data_files/pufs/h161ssp.zip
    URL for MEPS HC-160I: Appendix to MEPS 2013 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-160I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h160if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h160if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h160if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h160if2ssp.zip
    URL for MEPS HC-160H: 2013 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-160H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h160hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h160hssp.zip
    URL for MEPS HC-160G: 2013 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-160G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h160gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h160gssp.zip
    URL for MEPS HC-160F: 2013 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-160F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h160fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h160fssp.zip
    URL for MEPS HC-160E: 2013 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-160E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h160edat.zip
    https://meps.ahrq.gov/data_files/pufs/h160essp.zip
    URL for MEPS HC-160D: 2013 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-160D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h160ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h160dssp.zip
    URL for MEPS HC-160C: 2013 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-160C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h160cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h160cssp.zip
    URL for MEPS HC-160B: 2013  Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-160B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h160bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h160bssp.zip
    URL for MEPS HC-160A: 2013 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-160A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h160adat.zip
    https://meps.ahrq.gov/data_files/pufs/h160assp.zip
    URL for MEPS HC-159: 2014 P18R3/P19R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-159
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h159dat.zip
    https://meps.ahrq.gov/data_files/pufs/h159ssp.zip
    URL for MEPS HC-158: 2013 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-158
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h158dat.zip
    https://meps.ahrq.gov/data_files/pufs/h158ssp.zip
    URL for MEPS HC-157: 2013 Full Year Population Characteristics (HC-157 replaced by HC-163)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-157
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h157dat.zip
    https://meps.ahrq.gov/data_files/pufs/h157ssp.zip
    URL for MEPS HC-156: MEPS Panel 16 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-156
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h156dat.zip
    https://meps.ahrq.gov/data_files/pufs/h156ssp.zip
    URL for MEPS HC-155: 2012 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-155
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h155dat.zip
    https://meps.ahrq.gov/data_files/pufs/h155ssp.zip
    URL for MEPS HC-154: 2012 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-154
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h154dat.zip
    https://meps.ahrq.gov/data_files/pufs/h154ssp.zip
    URL for MEPS HC-153: 2012 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-153
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h153dat.zip
    https://meps.ahrq.gov/data_files/pufs/h153ssp.zip
    URL for MEPS HC-152I: Appendix to MEPS 2012 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-152I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h152if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h152if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h152if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h152if2ssp.zip
    URL for MEPS HC-152H: 2012 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-152H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h152hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h152hssp.zip
    URL for MEPS HC-152G: 2012 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-152G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h152gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h152gssp.zip
    URL for MEPS HC-152F: 2012 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-152F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h152fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h152fssp.zip
    URL for MEPS HC-152E: 2012 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-152E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h152edat.zip
    https://meps.ahrq.gov/data_files/pufs/h152essp.zip
    URL for MEPS HC-152D: 2012 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-152D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h152ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h152dssp.zip
    URL for MEPS HC-152C: 2012 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-152C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h152cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h152cssp.zip
    URL for MEPS HC-152B: 2012 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-152B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h152bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h152bssp.zip
    URL for MEPS HC-152A: 2012 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-152A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h152adat.zip
    https://meps.ahrq.gov/data_files/pufs/h152assp.zip
    URL for MEPS HC-151: 2013 P17R3/P18R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-151
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h151dat.zip
    https://meps.ahrq.gov/data_files/pufs/h151ssp.zip
    URL for MEPS HC-150: 2012 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-150
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h150dat.zip
    https://meps.ahrq.gov/data_files/pufs/h150ssp.zip
    URL for MEPS HC-149: 2012 Full Year Population Characteristics (HC-149 replaced by HC-155)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-149
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h149dat.zip
    https://meps.ahrq.gov/data_files/pufs/h149ssp.zip
    URL for MEPS HC-148: MEPS Panel 15 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-148
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h148dat.zip
    https://meps.ahrq.gov/data_files/pufs/h148ssp.zip
    URL for MEPS HC-147: 2011 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-147
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h147dat.zip
    https://meps.ahrq.gov/data_files/pufs/h147ssp.zip
    URL for MEPS HC-146: 2011 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-146
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h146dat.zip
    https://meps.ahrq.gov/data_files/pufs/h146ssp.zip
    URL for MEPS HC-145: 2011 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-145
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h145dat.zip
    https://meps.ahrq.gov/data_files/pufs/h145ssp.zip
    URL for MEPS HC-144I: Appendix to MEPS 2011 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-144I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h144if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h144if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h144if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h144if2ssp.zip
    URL for MEPS HC-144H: 2011 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-144H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h144hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h144hssp.zip
    URL for MEPS HC-144G: 2011 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-144G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h144gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h144gssp.zip
    URL for MEPS HC-144F: 2011 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-144F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h144fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h144fssp.zip
    URL for MEPS HC-144E: 2011 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-144E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h144edat.zip
    https://meps.ahrq.gov/data_files/pufs/h144essp.zip
    URL for MEPS HC-144D: 2011 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-144D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h144ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h144dssp.zip
    URL for MEPS HC-144C: 2011 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-144C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h144cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h144cssp.zip
    URL for MEPS HC-144B: 2011 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-144B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h144bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h144bssp.zip
    URL for MEPS HC-144A: 2011 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-144A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h144adat.zip
    https://meps.ahrq.gov/data_files/pufs/h144assp.zip
    URL for MEPS HC-143: 2012 P16R3/P17R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-143
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h143dat.zip
    https://meps.ahrq.gov/data_files/pufs/h143ssp.zip
    URL for MEPS HC-142: 2011 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-142
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h142dat.zip
    https://meps.ahrq.gov/data_files/pufs/h142ssp.zip
    URL for MEPS HC-141: 2011 Full Year Population Characteristics (HC-141 replaced by HC-147)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-141
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h141dat.zip
    https://meps.ahrq.gov/data_files/pufs/h141ssp.zip
    URL for MEPS HC-140: 2002-2009 Risk Adjustment Scores File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-140
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h140dat.zip
    https://meps.ahrq.gov/data_files/pufs/h140ssp.zip
    URL for MEPS HC-139: MEPS Panel 14 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-139
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h139dat.zip
    https://meps.ahrq.gov/data_files/pufs/h139ssp.zip
    URL for MEPS HC-138: 2010 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-138
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h138dat.zip
    https://meps.ahrq.gov/data_files/pufs/h138ssp.zip
    URL for MEPS HC-137: 2010 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-137
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h137dat.zip
    https://meps.ahrq.gov/data_files/pufs/h137ssp.zip
    URL for MEPS HC-136: 2010 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-136
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h136dat.zip
    https://meps.ahrq.gov/data_files/pufs/h136ssp.zip
    URL for MEPS HC-135I: Appendix to MEPS 2010 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-135I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h135if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h135if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h135if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h135if2ssp.zip
    URL for MEPS HC-135H: 2010 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-135H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h135hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h135hssp.zip
    URL for MEPS HC-135G: 2010 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-135G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h135gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h135gssp.zip
    URL for MEPS HC-135F: 2010 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-135F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h135fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h135fssp.zip
    URL for MEPS HC-135E: 2010 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-135E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h135edat.zip
    https://meps.ahrq.gov/data_files/pufs/h135essp.zip
    URL for MEPS HC-135D: 2010 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-135D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h135ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h135dssp.zip
    URL for MEPS HC-135C: 2010 Other Medical Expenses
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-135C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h135cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h135cssp.zip
    URL for MEPS HC-135B: 2010 Dental Visits
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-135B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h135bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h135bssp.zip
    URL for MEPS HC-135A: 2010 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-135A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h135adat.zip
    https://meps.ahrq.gov/data_files/pufs/h135assp.zip
    URL for MEPS HC-134: 2011 P15R3/P16R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-134
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h134dat.zip
    https://meps.ahrq.gov/data_files/pufs/h134ssp.zip
    URL for MEPS HC-133: 2010 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-133
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h133dat.zip
    https://meps.ahrq.gov/data_files/pufs/h133ssp.zip
    URL for MEPS HC-132: 2010 Full Year Population Characteristics (HC-132 replaced by HC-138)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-132
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h132dat.zip
    https://meps.ahrq.gov/data_files/pufs/h132ssp.zip
    URL for MEPS HC-131: 2000-2013 Employment Variables  File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-131
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h131dat.zip
    https://meps.ahrq.gov/data_files/pufs/h131ssp.zip
    URL for MEPS HC-130: MEPS Panel 13 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-130
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h130dat.zip
    https://meps.ahrq.gov/data_files/pufs/h130ssp.zip
    URL for MEPS HC-129: 2009 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-129
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h129dat.zip
    https://meps.ahrq.gov/data_files/pufs/h129ssp.zip
    URL for MEPS HC-128: 2009 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-128
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h128dat.zip
    https://meps.ahrq.gov/data_files/pufs/h128ssp.zip
    URL for MEPS HC-127: 2009 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-127
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h127dat.zip
    https://meps.ahrq.gov/data_files/pufs/h127ssp.zip
    URL for MEPS HC-126I: Appendix to MEPS 2009 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-126I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h126if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h126if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h126if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h126if2ssp.zip
    URL for MEPS HC-126H: 2009 Home Health File (Final)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-126H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h126hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h126hssp.zip
    URL for MEPS HC-126G: 2009 Office-Based Medical Provider Visits File (Final)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-126G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h126gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h126gssp.zip
    URL for MEPS HC-126F: 2009 Outpatient Visits File (Final)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-126F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h126fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h126fssp.zip
    URL for MEPS HC-126E: 2009 Emergency Room Visits File (Final)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-126E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h126edat.zip
    https://meps.ahrq.gov/data_files/pufs/h126essp.zip
    URL for MEPS HC-126D: 2009 Hospital Inpatient Stays File (Final)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-126D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h126ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h126dssp.zip
    URL for MEPS HC-126C: 2009 Other Medical Expenses
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-126C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h126cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h126cssp.zip
    URL for MEPS HC-126B: 2009 Dental Visits
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-126B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h126bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h126bssp.zip
    URL for MEPS HC-126A: 2009 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-126A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h126adat.zip
    https://meps.ahrq.gov/data_files/pufs/h126assp.zip
    URL for MEPS HC-125: 2010 P14R3/P15R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-125
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h125dat.zip
    https://meps.ahrq.gov/data_files/pufs/h125ssp.zip
    URL for MEPS HC-124: 2009 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-124
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h124dat.zip
    https://meps.ahrq.gov/data_files/pufs/h124ssp.zip
    URL for MEPS HC-123: 2009 Full Year Population Characteristics (HC-123 replaced by HC-129)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-123
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h123dat.zip
    https://meps.ahrq.gov/data_files/pufs/h123ssp.zip
    URL for MEPS HC-122: MEPS Panel 12 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-122
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h122dat.zip
    https://meps.ahrq.gov/data_files/pufs/h122ssp.zip
    URL for MEPS HC-121: 2008 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-121
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h121dat.zip
    https://meps.ahrq.gov/data_files/pufs/h121ssp.zip
    URL for MEPS HC-120: 2008 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-120
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h120dat.zip
    https://meps.ahrq.gov/data_files/pufs/h120ssp.zip
    URL for MEPS HC-119: 2008 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-119
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h119dat.zip
    https://meps.ahrq.gov/data_files/pufs/h119ssp.zip
    URL for MEPS HC-118I: Appendix to MEPS 2008 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-118I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h118if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h118if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h118if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h118if2ssp.zip
    URL for MEPS HC-118H: 2008 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-118H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h118hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h118hssp.zip
    URL for MEPS HC-118G: 2008 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-118G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h118gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h118gssp.zip
    URL for MEPS HC-118F: 2008 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-118F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h118fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h118fssp.zip
    URL for MEPS HC-118E: 2008 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-118E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h118edat.zip
    https://meps.ahrq.gov/data_files/pufs/h118essp.zip
    URL for MEPS HC-118D: 2008 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-118D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h118ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h118dssp.zip
    URL for MEPS HC-118C: 2008 Other Medical Expenses
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-118C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h118cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h118cssp.zip
    URL for MEPS HC-118B: 2008 Dental Visits
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-118B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h118bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h118bssp.zip
    URL for MEPS HC-118A: 2008 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-118A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h118adat.zip
    https://meps.ahrq.gov/data_files/pufs/h118assp.zip
    URL for MEPS HC-117: 2009 P13R3/P14R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-117
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h117dat.zip
    https://meps.ahrq.gov/data_files/pufs/h117ssp.zip
    URL for MEPS HC-116: 2008 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-116
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h116dat.zip
    https://meps.ahrq.gov/data_files/pufs/h116ssp.zip
    URL for MEPS HC-115: 2008 Full Year Population Characteristics (HC-115 replaced by HC-121)
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-115
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h115dat.zip
    https://meps.ahrq.gov/data_files/pufs/h115ssp.zip
    URL for MEPS HC-114: MEPS Panel 11 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-114
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h114dat.zip
    https://meps.ahrq.gov/data_files/pufs/h114ssp.zip
    URL for MEPS HC-113: 2007 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-113
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h113dat.zip
    https://meps.ahrq.gov/data_files/pufs/h113ssp.zip
    URL for MEPS HC-112: 2007 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-112
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h112dat.zip
    https://meps.ahrq.gov/data_files/pufs/h112ssp.zip
    URL for MEPS HC-111: 2007 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-111
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h111dat.zip
    https://meps.ahrq.gov/data_files/pufs/h111ssp.zip
    URL for MEPS HC-110I: Appendix to MEPS 2007 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-110I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h110if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h110if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h110if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h110if2ssp.zip
    URL for MEPS HC-110H: 2007 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-110H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h110hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h110hssp.zip
    URL for MEPS HC-110G: 2007 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-110G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h110gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h110gssp.zip
    URL for MEPS HC-110F: 2007 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-110F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h110fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h110fssp.zip
    URL for MEPS HC-110E: 2007 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-110E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h110edat.zip
    https://meps.ahrq.gov/data_files/pufs/h110essp.zip
    URL for MEPS HC-110D: 2007 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-110D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h110ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h110dssp.zip
    URL for MEPS HC-110C: 2007 Other Medical Expenses
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-110C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h110cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h110cssp.zip
    URL for MEPS HC-110B: 2007 Dental Visits
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-110B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h110bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h110bssp.zip
    URL for MEPS HC-110A: 2007 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-110A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h110adat.zip
    https://meps.ahrq.gov/data_files/pufs/h110assp.zip
    URL for MEPS HC-109: 2008 P12R3/P13R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-109
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h109dat.zip
    https://meps.ahrq.gov/data_files/pufs/h109ssp.zip
    URL for MEPS HC-108: 2007 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-108
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h108dat.zip
    https://meps.ahrq.gov/data_files/pufs/h108ssp.zip
    URL for MEPS HC-106: MEPS Panel 10 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-106
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h106dat.zip
    https://meps.ahrq.gov/data_files/pufs/h106ssp.zip
    URL for MEPS HC-105: 2006 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-105
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h105dat.zip
    https://meps.ahrq.gov/data_files/pufs/h105ssp.zip
    URL for MEPS HC-104: 2006 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-104
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h104dat.zip
    https://meps.ahrq.gov/data_files/pufs/h104ssp.zip
    URL for MEPS HC-103: 2006 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-103
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h103dat.zip
    https://meps.ahrq.gov/data_files/pufs/h103ssp.zip
    URL for MEPS HC-102I: Appendix to MEPS 2006 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-102I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h102if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h102if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h102if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h102if2ssp.zip
    URL for MEPS HC-102H: 2006 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-102H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h102hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h102hssp.zip
    URL for MEPS HC-102G: 2006 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-102G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h102gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h102gssp.zip
    URL for MEPS HC-102F: 2006 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-102F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h102fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h102fssp.zip
    URL for MEPS HC-102E: 2006 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-102E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h102edat.zip
    https://meps.ahrq.gov/data_files/pufs/h102essp.zip
    URL for MEPS HC-102D: 2006 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-102D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h102ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h102dssp.zip
    URL for MEPS HC-102C: 2006 Other Medical Expenses
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-102C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h102cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h102cssp.zip
    URL for MEPS HC-102B: 2006 Dental Visits
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-102B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h102bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h102bssp.zip
    URL for MEPS HC-102A: 2006 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-102A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h102adat.zip
    https://meps.ahrq.gov/data_files/pufs/h102assp.zip
    URL for MEPS HC-101: 2007 P11R3/P12R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-101
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h101dat.zip
    https://meps.ahrq.gov/data_files/pufs/h101ssp.zip
    URL for MEPS HC-100: 2006 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-100
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h100dat.zip
    https://meps.ahrq.gov/data_files/pufs/h100ssp.zip
    URL for MEPS HC-098: MEPS Panel 9 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-098
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h98dat.zip
    https://meps.ahrq.gov/data_files/pufs/h98ssp.zip
    URL for MEPS HC-097: 2005 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-097
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h97dat.zip
    https://meps.ahrq.gov/data_files/pufs/h97ssp.zip
    URL for MEPS HC-096: 2005 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-096
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h96dat.zip
    https://meps.ahrq.gov/data_files/pufs/h96ssp.zip
    URL for MEPS HC-095: 2005 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-095
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h95dat.zip
    https://meps.ahrq.gov/data_files/pufs/h95ssp.zip
    URL for MEPS HC-094I: Appendix to MEPS 2005 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-094I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h94if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h94if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h94if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h94if2ssp.zip
    URL for MEPS HC-094H: 2005 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-094H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h94hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h94hssp.zip
    URL for MEPS HC-094G: 2005 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-094G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h94gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h94gssp.zip
    URL for MEPS HC-094F: 2005 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-094F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h94fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h94fssp.zip
    URL for MEPS HC-094E: 2005 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-094E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h94edat.zip
    https://meps.ahrq.gov/data_files/pufs/h94essp.zip
    URL for MEPS HC-094D: 2005 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-094D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h94ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h94dssp.zip
    URL for MEPS HC-094C: 2005 Other Medical Expenses
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-094C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h94cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h94cssp.zip
    URL for MEPS HC-094B: 2005 Dental Visits
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-094B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h94bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h94bssp.zip
    URL for MEPS HC-094A: 2005 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-094A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h94adat.zip
    https://meps.ahrq.gov/data_files/pufs/h94assp.zip
    URL for MEPS HC-093: 2006 P10R3/P11R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-093
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h93dat.zip
    https://meps.ahrq.gov/data_files/pufs/h93ssp.zip
    URL for MEPS HC-092: 1996-2004 Risk Adjustment Scores File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-092
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h92dat.zip
    https://meps.ahrq.gov/data_files/pufs/h92ssp.zip
    URL for MEPS HC-091: 2005 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-091
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h91dat.zip
    https://meps.ahrq.gov/data_files/pufs/h91ssp.zip
    URL for MEPS HC-089: 2004 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-089
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h89dat.zip
    https://meps.ahrq.gov/data_files/pufs/h89ssp.zip
    URL for MEPS HC-088: 2004 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-088
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h88dat.zip
    https://meps.ahrq.gov/data_files/pufs/h88ssp.zip
    URL for MEPS HC-087: 2004 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-087
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h87dat.zip
    https://meps.ahrq.gov/data_files/pufs/h87ssp.zip
    URL for MEPS HC-086: MEPS Panel 8 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-086
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h86dat.zip
    https://meps.ahrq.gov/data_files/pufs/h86ssp.zip
    URL for MEPS HC-085I: Appendix to MEPS 2004 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-085I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h85if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h85if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h85if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h85if2ssp.zip
    URL for MEPS HC-085H: 2004 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-085H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h85hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h85hssp.zip
    URL for MEPS HC-085G: 2004 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-085G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h85gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h85gssp.zip
    URL for MEPS HC-085F: 2004 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-085F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h85fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h85fssp.zip
    URL for MEPS HC-085E: 2004 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-085E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h85edat.zip
    https://meps.ahrq.gov/data_files/pufs/h85essp.zip
    URL for MEPS HC-085D: 2004 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-085D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h85ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h85dssp.zip
    URL for MEPS HC-085C: 2004 Other Medical Expenses
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-085C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h85cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h85cssp.zip
    URL for MEPS HC-085B: 2004 Dental Visits
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-085B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h85bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h85bssp.zip
    URL for MEPS HC-085A: 2004 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-085A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h85adat.zip
    https://meps.ahrq.gov/data_files/pufs/h85assp.zip
    URL for MEPS HC-084: 2005 P9R3/P10R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-084
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h84dat.zip
    https://meps.ahrq.gov/data_files/pufs/h84ssp.zip
    URL for MEPS HC-083: 2004 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-083
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h83dat.zip
    https://meps.ahrq.gov/data_files/pufs/h83ssp.zip
    URL for MEPS HC-080: MEPS Panel 7 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-080
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h80dat.zip
    https://meps.ahrq.gov/data_files/pufs/h80ssp.zip
    URL for MEPS HC-079: 2003 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-079
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h79dat.zip
    https://meps.ahrq.gov/data_files/pufs/h79ssp.zip
    URL for MEPS HC-078: 2003 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-078
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h78dat.zip
    https://meps.ahrq.gov/data_files/pufs/h78ssp.zip
    URL for MEPS HC-077I: Appendix to MEPS 2003 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-077I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h77if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h77if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h77if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h77if2ssp.zip
    URL for MEPS HC-077H: 2003 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-077H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h77hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h77hssp.zip
    URL for MEPS HC-077G: 2003 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-077G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h77gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h77gssp.zip
    URL for MEPS HC-077F: 2003 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-077F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h77fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h77fssp.zip
    URL for MEPS HC-077E: 2003 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-077E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h77edat.zip
    https://meps.ahrq.gov/data_files/pufs/h77essp.zip
    URL for MEPS HC-077D: 2003 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-077D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h77ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h77dssp.zip
    URL for MEPS HC-077C: 2003 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-077C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h77cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h77cssp.zip
    URL for MEPS HC-077B: 2003 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-077B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h77bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h77bssp.zip
    URL for MEPS HC-077A: 2003 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-077A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h77adat.zip
    https://meps.ahrq.gov/data_files/pufs/h77assp.zip
    URL for MEPS HC-076: 2003 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-076
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h76dat.zip
    https://meps.ahrq.gov/data_files/pufs/h76ssp.zip
    URL for MEPS HC-075: 2004 P8R3/P9R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-075
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h75dat.zip
    https://meps.ahrq.gov/data_files/pufs/h75ssp.zip
    URL for MEPS HC-074: 2003 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-074
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h74dat.zip
    https://meps.ahrq.gov/data_files/pufs/h74ssp.zip
    URL for MEPS HC-071: MEPS Panel 6 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-071
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h71dat.zip
    https://meps.ahrq.gov/data_files/pufs/h71ssp.zip
    URL for MEPS HC-070: 2002 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-070
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h70dat.zip
    https://meps.ahrq.gov/data_files/pufs/h70ssp.zip
    URL for MEPS HC-069: 2002 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-069
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h69dat.zip
    https://meps.ahrq.gov/data_files/pufs/h69ssp.zip
    URL for MEPS HC-068: Multum Lexicon Addendum Files to MEPS Prescribed Medicines Files 1996-2013
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-068
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h68f1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f3dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f4dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f5dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f6dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f7dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f8dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f9dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f10dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f11dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f12dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f13dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f14dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f15dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f16dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f17dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f18dat.zip
    https://meps.ahrq.gov/data_files/pufs/h68f1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f2ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f3ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f4ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f5ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f6ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f7ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f8ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f9ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f10ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f11ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f12ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f13ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f14ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f15ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f16ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f17ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h68f18ssp.zip
    URL for MEPS HC-067I: Appendix to MEPS 2002 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-067I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h67if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h67if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h67if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h67if2ssp.zip
    URL for MEPS HC-067H: 2002 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-067H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h67hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h67hssp.zip
    URL for MEPS HC-067G: 2002 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-067G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h67gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h67gssp.zip
    URL for MEPS HC-067F: 2002 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-067F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h67fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h67fssp.zip
    URL for MEPS HC-067E: 2002 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-067E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h67edat.zip
    https://meps.ahrq.gov/data_files/pufs/h67essp.zip
    URL for MEPS HC-067D: 2002 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-067D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h67ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h67dssp.zip
    URL for MEPS HC-067C: 2002 Other Medical Expenses
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-067C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h67cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h67cssp.zip
    URL for MEPS HC-067B: 2002 Dental Visits
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-067B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h67bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h67bssp.zip
    URL for MEPS HC-067A: 2002 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-067A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h67adat.zip
    https://meps.ahrq.gov/data_files/pufs/h67assp.zip
    URL for MEPS HC-066: 2002 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-066
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h66dat.zip
    https://meps.ahrq.gov/data_files/pufs/h66ssp.zip
    URL for MEPS HC-065: MEPS Panel 5 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-065
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h65dat.zip
    https://meps.ahrq.gov/data_files/pufs/h65ssp.zip
    URL for MEPS HC-064: 2003 P7R3/P8R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-064
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h64dat.zip
    https://meps.ahrq.gov/data_files/pufs/h64ssp.zip
    URL for MEPS HC-063: 2002 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-063
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h63dat.zip
    https://meps.ahrq.gov/data_files/pufs/h63ssp.zip
    URL for MEPS HC-061: 2001 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-061
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h61dat.zip
    https://meps.ahrq.gov/data_files/pufs/h61ssp.zip
    URL for MEPS HC-060: 2001 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-060
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h60dat.zip
    https://meps.ahrq.gov/data_files/h60ssp.zip
    URL for MEPS HC-059I: Appendix to MEPS 2001 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-059I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h59if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h59if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h59if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h59if2ssp.zip
    URL for MEPS HC-059H: 2001 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-059H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h59hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h59hssp.zip
    URL for MEPS HC-059G: 2001 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-059G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h59gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h59gssp.zip
    URL for MEPS HC-059F: 2001 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-059F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h59fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h59fssp.zip
    URL for MEPS HC-059E: 2001 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-059E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h59edat.zip
    https://meps.ahrq.gov/data_files/pufs/h59essp.zip
    URL for MEPS HC-059D: 2001 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-059D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h59ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h59dssp.zip
    URL for MEPS HC-059C: 2001 Other Medical Expenses
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-059C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h59cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h59cssp.zip
    URL for MEPS HC-059B: 2001 Dental Visits
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-059B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h59bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h59bssp.zip
    URL for MEPS HC-059A: 2001 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-059A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h59adat.zip
    https://meps.ahrq.gov/data_files/pufs/h59assp.zip
    URL for MEPS HC-058: MEPS Panel 4 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-058
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h58dat.zip
    https://meps.ahrq.gov/data_files/pufs/h58ssp.zip
    URL for MEPS HC-057: 2001 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-057
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h57dat.zip
    https://meps.ahrq.gov/data_files/pufs/h57ssp.zip
    URL for MEPS HC-056: 2001 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-056
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h56dat.zip
    https://meps.ahrq.gov/data_files/pufs/h56ssp.zip
    URL for MEPS HC-053: 2002 P6R3/P7R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-053
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h53dat.zip
    https://meps.ahrq.gov/data_files/pufs/h53ssp.zip
    URL for MEPS HC-052: 2000 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-052
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h52dat.zip
    https://meps.ahrq.gov/data_files/pufs/h52ssp.zip
    URL for MEPS HC-051I: Appendix to MEPS 2000 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-051I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h51if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h51if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h51if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h51if2ssp.zip
    URL for MEPS HC-051H: 2000 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-051H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h51hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h51hssp.zip
    URL for MEPS HC-051G: 2000 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-051G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h51gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h51gssp.zip
    URL for MEPS HC-051F: 2000 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-051F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h51fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h51fssp.zip
    URL for MEPS HC-051E: 2000 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-051E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h51edat.zip
    https://meps.ahrq.gov/data_files/pufs/h51essp.zip
    URL for MEPS HC-051D: 2000 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-051D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h51ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h51dssp.zip
    URL for MEPS HC-051C: 2000 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-051C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h51cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h51cssp.zip
    URL for MEPS HC-051B: 2000 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-051B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h51bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h51bssp.zip
    URL for MEPS HC-051A: 2000 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-051A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h51adat.zip
    https://meps.ahrq.gov/data_files/pufs/h51assp.zip
    URL for MEPS HC-050: 2000 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-050
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h50dat.zip
    https://meps.ahrq.gov/data_files/pufs/h50ssp.zip
    URL for MEPS HC-049: 1998 Long Term Care
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-049
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h49dat.zip
    https://meps.ahrq.gov/data_files/pufs/h49ssp.zip
    URL for MEPS HC-048: MEPS Panel 3 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-048
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h48dat.zip
    https://meps.ahrq.gov/data_files/pufs/h48ssp.zip
    URL for MEPS HC-047: 1997-2000 Person Round Plan Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-047
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h47f1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h47f2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h47f3dat.zip
    https://meps.ahrq.gov/data_files/pufs/h47f4dat.zip
    https://meps.ahrq.gov/data_files/pufs/h47f1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h47f2ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h47f3ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h47f4ssp.zip
    URL for MEPS HC-044: 1999 Supplemental Public Use File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-044
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h44dat.zip
    https://meps.ahrq.gov/data_files/pufs/h44ssp.zip
    URL for MEPS HC-043: 1998 Supplemental Public Use File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-043
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h43f1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h43f2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h43f1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h43f2ssp.zip
    URL for MEPS HC-042: 1997 Supplemental Public Use File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-042
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h42f1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h42f2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h42f3dat.zip
    https://meps.ahrq.gov/data_files/pufs/h42f1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h42f2ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h42f3ssp.zip
    URL for MEPS HC-041: 1996 Supplemental Public Use File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-041
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h41dat.zip
    https://meps.ahrq.gov/data_files/pufs/h41ssp.zip
    URL for MEPS HC-040: 2000 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-040
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h40dat.zip
    https://meps.ahrq.gov/data_files/pufs/h40ssp.zip
    URL for MEPS HC-038: 1999 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-038
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h38dat.zip
    https://meps.ahrq.gov/data_files/pufs/h38ssp.zip
    URL for MEPS HC-037: 1999 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-037
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h37dat.zip
    https://meps.ahrq.gov/data_files/pufs/h37ssp.zip
    URL for MEPS HC-036BRR: MEPS 1996-2020 Replicate File for BRR Variance Estimation
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-036BRR
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h036brr/h36brr20dat.zip
    https://meps.ahrq.gov/data_files/pufs/h036brr/h36brr20ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h036brr/h36brr20v9.zip
    https://meps.ahrq.gov/data_files/pufs/h036brr/h36brr20dta.zip
    https://meps.ahrq.gov/data_files/pufs/h036brr/h36brr20xlsx.zip
    URL for MEPS HC-036: MEPS 1996-2020 Pooled Linkage File for Common Variance Structure
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-036
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h036/h36u20dat.zip
    https://meps.ahrq.gov/data_files/pufs/h036/h36u20ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h036/h36u20v9.zip
    https://meps.ahrq.gov/data_files/pufs/h036/h36u20dta.zip
    https://meps.ahrq.gov/data_files/pufs/h036/h36u20xlsx.zip
    URL for MEPS HC-035: MEPS Panel 2 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-035
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h35dat.zip
    https://meps.ahrq.gov/data_files/pufs/h35ssp.zip
    URL for MEPS HC-034: 2001 P5R3/P6R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-034
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h34dat.zip
    https://meps.ahrq.gov/data_files/pufs/h34ssp.zip
    URL for MEPS HC-033I: Appendix to MEPS 1999 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-033I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h33if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h33if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h33if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h33if2ssp.zip
    URL for MEPS HC-033H: 1999 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-033H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h33hdat.zip
    https://meps.ahrq.gov/data_files/pufs/h33hssp.zip
    URL for MEPS HC-033G: 1999 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-033G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h33gdat.zip
    https://meps.ahrq.gov/data_files/pufs/h33gssp.zip
    URL for MEPS HC-033F: 1999 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-033F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h33fdat.zip
    https://meps.ahrq.gov/data_files/pufs/h33fssp.zip
    URL for MEPS HC-033E: 1999 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-033E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h33edat.zip
    https://meps.ahrq.gov/data_files/pufs/h33essp.zip
    URL for MEPS HC-033D: 1999 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-033D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h33ddat.zip
    https://meps.ahrq.gov/data_files/pufs/h33dssp.zip
    URL for MEPS HC-033C: 1999 Other Medical Expenses
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-033C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h33cdat.zip
    https://meps.ahrq.gov/data_files/pufs/h33cssp.zip
    URL for MEPS HC-033B: 1999 Dental Visits
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-033B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h33bdat.zip
    https://meps.ahrq.gov/data_files/pufs/h33bssp.zip
    URL for MEPS HC-033A: 1999 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-033A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h33adat.zip
    https://meps.ahrq.gov/data_files/pufs/h33assp.zip
    URL for MEPS HC-032: 1999 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-032
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h32dat.zip
    https://meps.ahrq.gov/data_files/pufs/h32ssp.zip
    URL for MEPS HC-028: 1998 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-028
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h28dat.zip
    https://meps.ahrq.gov/data_files/pufs/h28ssp.zip
    URL for MEPS HC-027: 1998 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-027
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h27dat.zip
    https://meps.ahrq.gov/data_files/pufs/h27ssp.zip
    URL for MEPS HC-026I: Appendix to MEPS 1998 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-026I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h26if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h26if2ssp.zip
    URL for MEPS HC-026H: 1998 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-026H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h26hf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26hf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26hf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h26hf2ssp.zip
    URL for MEPS HC-026G: 1998 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-026G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h26gf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26gf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26gf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h26gf2ssp.zip
    URL for MEPS HC-026F: 1998 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-026F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h26ff1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26ff2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26ff1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h26ff2ssp.zip
    URL for MEPS HC-026E: 1998 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-026E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h26ef1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26ef2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26ef1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h26ef2ssp.zip
    URL for MEPS HC-026D: 1998 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-026D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h26df1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26df2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26df1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h26df2ssp.zip
    URL for MEPS HC-026C: 1998 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-026C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h26cf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26cf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26cf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h26cf2ssp.zip
    URL for MEPS HC-026B: 1998 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-026B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h26bf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26bf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h26bf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h26bf2ssp.zip
    URL for MEPS HC-026A: 1998 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-026A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h26adat.zip
    https://meps.ahrq.gov/data_files/pufs/h26assp.zip
    URL for MEPS HC-025: 1998 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-025
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h25dat.zip
    https://meps.ahrq.gov/data_files/pufs/h25ssp.zip
    URL for MEPS HC-024: 1996 Person Round Plan File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-024
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h24dat.zip
    https://meps.ahrq.gov/data_files/pufs/h24ssp.zip
    URL for MEPS HC-023: MEPS Panel 1 Longitudinal Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-023
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h23dat.zip
    https://meps.ahrq.gov/data_files/pufs/h23ssp.zip
    URL for MEPS HC-022: 2000 P4R3/P5R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-022
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h22dat.zip
    https://meps.ahrq.gov/data_files/pufs/h22ssp.zip
    URL for MEPS HC-020: 1997 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-020
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h20dat.zip
    https://meps.ahrq.gov/data_files/pufs/h20ssp.zip
    URL for MEPS HC-019: 1997 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-019
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h19dat.zip
    https://meps.ahrq.gov/data_files/pufs/h19ssp.zip
    URL for MEPS HC-018: 1997 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-018
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h18dat.zip
    https://meps.ahrq.gov/data_files/pufs/h18ssp.zip
    URL for MEPS HC-017: 1996 Health Insurance Plan Abstraction Linked Data
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-017
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h17dat.zip
    https://meps.ahrq.gov/data_files/pufs/h17ssp.zip
    URL for MEPS HC-016I: Appendix to MEPS 1997 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-016I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h16if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h16if2ssp.zip
    URL for MEPS HC-016H: 1997 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-016H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h16hf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16hf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16hf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h16hf2ssp.zip
    URL for MEPS HC-016G: 1997 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-016G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h16gf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16gf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16gf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h16gf2ssp.zip
    URL for MEPS HC-016F: 1997 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-016F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h16ff1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16ff2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16ff1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h16ff2ssp.zip
    URL for MEPS HC-016E: 1997 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-016E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h16ef1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16ef2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16ef1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h16ef2ssp.zip
    URL for MEPS HC-016D: 1997 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-016D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h16df1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16df2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16df1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h16df2ssp.zip
    URL for MEPS HC-016C: 1997 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-016C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h16cf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16cf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16cf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h16cf2ssp.zip
    URL for MEPS HC-016B: 1997 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-016B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h16bf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16bf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h16bf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h16bf2ssp.zip
    URL for MEPS HC-016A: 1997 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-016A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h16adat.zip
    https://meps.ahrq.gov/data_files/pufs/h16assp.zip
    URL for MEPS HC-013: 1999 P4R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-013
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h13dat.zip
    https://meps.ahrq.gov/data_files/pufs/h13ssp.zip
    URL for MEPS HC-012: 1996 Full Year Consolidated Data File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-012
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h12dat.zip
    https://meps.ahrq.gov/data_files/pufs/h12ssp.zip
    URL for MEPS HC-010I: Appendix to MEPS 1996 Event Files
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-010I
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h10if1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10if2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10if1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h10if2ssp.zip
    URL for MEPS HC-010H: 1996 Home Health File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-010H
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h10hf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10hf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10hf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h10hf2ssp.zip
    URL for MEPS HC-010G: 1996 Office-Based Medical Provider Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-010G
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h10gf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10gf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10gf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h10gf2ssp.zip
    URL for MEPS HC-010F: 1996 Outpatient Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-010F
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h10ff1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10ff2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10ff1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h10ff2ssp.zip
    URL for MEPS HC-010E: 1996 Emergency Room Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-010E
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h10ef1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10ef2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10ef1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h10ef2ssp.zip
    URL for MEPS HC-010D: 1996 Hospital Inpatient Stays File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-010D
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h10df1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10df2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10df1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h10df2ssp.zip
    URL for MEPS HC-010C: 1996 Other Medical Expenses File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-010C
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h10cf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10cf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10cf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h10cf2ssp.zip
    URL for MEPS HC-010B: 1996 Dental Visits File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-010B
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h10bf1dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10bf2dat.zip
    https://meps.ahrq.gov/data_files/pufs/h10bf1ssp.zip
    https://meps.ahrq.gov/data_files/pufs/h10bf2ssp.zip
    URL for MEPS HC-010A: 1996 Prescribed Medicines File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-010A
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h10adat.zip
    https://meps.ahrq.gov/data_files/pufs/h10assp.zip
    URL for MEPS HC-009: 1998 P2R3/P3R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-009
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h09dat.zip
    https://meps.ahrq.gov/data_files/pufs/h09ssp.zip
    URL for MEPS HC-007: 1996 Jobs File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-007
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h07dat.zip
    https://meps.ahrq.gov/data_files/pufs/h07ssp.zip
    URL for MEPS HC-006R: 1996 Medical Conditions File
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-006R
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h06rdat.zip
    https://meps.ahrq.gov/data_files/pufs/h06rssp.zip
    URL for MEPS HC-005: 1997 P1R3/P2R1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-005
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h05dat.zip
    https://meps.ahrq.gov/data_files/pufs/h05ssp.zip
    URL for MEPS HC-001: 1996 Panel Round 1 Population Characteristics
    https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-001
    URLs for the data file in multiple formats, if available
    https://meps.ahrq.gov/data_files/pufs/h01dat.zip
    A total of 1,154  MEPS-HC data file format-specific URLs listed on the MEPS website
    


```python
!jupyter nbconvert --to html Final_Solution_Feb16_2023.ipynb
```

    [NbConvertApp] Converting notebook Final_Solution_Feb16_2023.ipynb to html
    [NbConvertApp] Writing 723525 bytes to Final_Solution_Feb16_2023.html
    


```python
!jupyter nbconvert --to md Final_Solution_Feb16_2023.ipynb
```


```python

```
