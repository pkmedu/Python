# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 23:05:14 2019

@author: PMuhuri
"""
import pandas as pd
#import html5lib as ht
url = "https://simple.wikipedia.org/wiki/List_of_U.S._states"
mylist = pd.read_html(url)
print(mylist)
#mydf = pd.DataFrame(mylist)
#print(mydf)
