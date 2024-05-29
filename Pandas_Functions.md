# $\textnormal{\color{red} Working with pandas (Python Data Analysis Library)}$

[Writing Parquet Files in Python with Pandas, PySpark, and Koalas](https://mungingdata.com/python/writing-parquet-pandas-pyspark-koalas/)

[Filtering Dataframes](https://www.dataquest.io/blog/filtering-pandas-dataframes/)

## Pandas Functions

The following Pandas functions (code and text) are selectively obtained from 
an article by Aryan Garg in KDnuggets Newsletter on November 10, 2023 
(https://www.kdnuggets.com/10-essential-pandas-functions-every-data-scientist-should-know).


1. Data Viewing
 
	1.	df.head() displays the first five rows of the sample data.
	2.	df.tail() displays the last five rows of the sample data.
	3.	df.sample(n) displays the random n number of rows in the sample data.
	4.	df.shape displays the sample data's rows and columns (dimensions).

2. Statistics

	1. df.describe() provides the basic statistics of each column of the sample data
	2. df.info() provides information about the various data types used and the non-null count of each column.
	3. df.corr() gives you the correlation matrix between all the integer columns in the data frame.
	4. df.memory_usage() tells you how much memory is being consumed by each column.

3. Data Selection

	1.	df.iloc[row_num] will select a particular row based on its index.
	2.	df[col_name] will select the particular column.
	3.	df[[‘col1’, ‘col2’]] will select multiple columns given.


4.	Data Cleaning

	1. df.isnull() will identify the missing values in your dataframe.
	2.df.dropna() will remove the rows containing missing values in any column.
	3. df.fillna(val) will fill the missing values with val given in the argument.
	4. df[‘col’].astype(new_data_type): It can convert the data type of the selected columns to a different data type.
	5. wadf[‘col’].astype(new_data_type)can convert the data type of the selected columns to a different data type.

5. Data Analysis

	1.	Aggregation Functions group a column by its name and then apply some aggregation functions like sum, min/max, mean, etc.
	2.	Filtering Data:  You can filter the data in rows based on a specific value or a condition.
	3.	Sorting Data: You can sort the data based on a specific column, either in ascending or descending order.
	4.	Pivot Tables: You can create pivot tables that summarize the data using specific columns. This type of tables is very useful in analyzing the data when you only want to consider the effect of particular columns.
	5.	Combining Data Frames: We can combine and merge several data frames either horizontally or vertically. It will concatenate two data frames and return a single merged data frame.
	6.	Applying Custom Functions: You can apply custom functions in either a row or a column according to your needs.
	7.	Applymap: We can also apply a custom function to every element of the dataframe in a single line of code. But a point to remember is that it applies to all the dataframe elements.

	8. Time Series Analysis: In mathematics, time series analysis means analyzing the data collected over a specific time interval, and pandas have functions to perform this type of analysis.
	9. Cross Tabulation: We can perform cross-tabulation between two columns of a table. It is generally a frequency table that shows the frequency of occurrences of various categories. It can help you to understand the distribution of categories across different regions.
	10. Handling Outliers: Outliers in data means that a particular point goes far beyond the average range.
	
	## Data Analysis Using Pandas/Python
	
	[Data Analysis in Python](https://dataanalysispython.readthedocs.io/en/latest/)
	
	[7 Pandas Plotting Functions for Quick Data Visualization](https://www.kdnuggets.com/7-pandas-plotting-functions-for-quick-data-visualization)

