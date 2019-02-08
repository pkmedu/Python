#!/usr/bin/env python
# coding: utf-8

# In[19]:


#https://www.andreagrandi.it/2018/04/14/machine-learning-pima-indians-diabetes/
# We import the libraries needed to read the dataset
import os
import pandas as pd
import numpy as np
os.getcwd()


# In[20]:


# We placed the dataset under datasets/ sub folder
PATH = 'D:\\my_py_scripts'
path_filename = os.path.join(PATH, 'pima-indians-diabetes.csv')
path_filename


# In[21]:


col_names = ["NumTimesPrg", "PlGlcConc", "BloodP",   "SkinThick", "TwoHourSerIns", "BMI",  "DiPedFunc", "Age", "HasDiabetes"]
dataset = pd.read_csv(path_filename, names=col_names)
dataset.shape
dataset.head()


# In[22]:


corr = dataset.corr()
corr
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
sns.heatmap(corr, annot = True)


# In[23]:


import matplotlib.pyplot as plt
dataset.hist(bins=50, figsize=(20, 15))
plt.show()


# In[24]:


# Calculate the median value for BMI
median_bmi = dataset['BMI'].median()
# Substitute it in the BMI column of the
# dataset where values are 0
dataset['BMI'] = dataset['BMI'].replace(
    to_replace=0, value=median_bmi)
median_bmi


# In[25]:


# Calculate the median value for BloodP
median_bloodp = dataset['BloodP'].median()
# Substitute it in the BloodP column of the
# dataset where values are 0
dataset['BloodP'] = dataset['BloodP'].replace(
    to_replace=0, value=median_bloodp)
median_bloodp


# In[26]:



# Calculate the median value for PlGlcConc
median_plglcconc = dataset['PlGlcConc'].median()
# Substitute it in the PlGlcConc column of the
# dataset where values are 0
dataset['PlGlcConc'] = dataset['PlGlcConc'].replace(
    to_replace=0, value=median_plglcconc)

median_plglcconc


# In[27]:


# Calculate the median value for SkinThick
median_skinthick = dataset['SkinThick'].median()
# Substitute it in the SkinThick column of the
# dataset where values are 0
dataset['SkinThick'] = dataset['SkinThick'].replace(
    to_replace=0, value=median_skinthick)
median_skinthick


# In[28]:


# Calculate the median value for TwoHourSerIns
median_twohourserins = dataset['TwoHourSerIns'].median()
# Substitute it in the TwoHourSerIns column of the
# dataset where values are 0
dataset['TwoHourSerIns'] = dataset['TwoHourSerIns'].replace(
    to_replace=0, value=median_twohourserins)
median_twohourserins


# In[29]:


# Split the training dataset in 80% / 20%
from sklearn.model_selection import train_test_split
train_set, test_set = train_test_split(
    dataset, test_size=0.2, random_state=42)


# In[30]:


# Separate labels from the rest of the dataset
train_set_labels = train_set["HasDiabetes"].copy()
train_set = train_set.drop("HasDiabetes", axis=1)

test_set_labels = test_set["HasDiabetes"].copy()
test_set = test_set.drop("HasDiabetes", axis=1)
test_set.head()


# In[34]:


# Apply a scaler
from sklearn.preprocessing import MinMaxScaler as Scaler

scaler = Scaler()
scaler.fit(train_set)
train_set_scaled = scaler.transform(train_set)
test_set_scaled = scaler.transform(test_set)
print(train_set_scaled)
print(test_set_scaled)
df = pd.DataFrame(data=train_set_scaled)
df.head()


# In[35]:


# Import all the algorithms we want to test
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeRegressor


# In[39]:


# Prepare an array with all the algorithms
models = []
models.append(('LR', LogisticRegression()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVC', SVC()))
models.append(('LSVC', LinearSVC()))
models.append(('RFC', RandomForestClassifier()))
models.append(('DTR', DecisionTreeRegressor()))
print(models)


# In[40]:


# Prepare the configuration to run the test
seed = 7
results = []
names = []
X = train_set_scaled
Y = train_set_labels
# Every algorithm is tested and results are
# collected and printed
from sklearn import model_selection 
for name, model in models:
    kfold = model_selection.KFold(
        n_splits=10, random_state=seed)
    cv_results = model_selection.cross_val_score(
        model, X, Y, cv=kfold, scoring='accuracy')
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (
        name, cv_results.mean(), cv_results.std())
    print(msg)


# In[41]:


# boxplot algorithm comparison
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()


# In[ ]:




