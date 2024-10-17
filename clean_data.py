import pandas as pd
import numpy as np
import tqdm
import argparse
import os

# set working directory
os.chdir("/Users/iriskim/Desktop/06-data-munging-irisk2050")

# load data
df = pd.read_csv("messy_population_data.csv")
df2 = df.copy()

# Issue 1: Invalid Data

## Replace the invalid values of income_groups with their corresponding valid values
df2['income_groups'] = df2['income_groups'].replace({'high_income_typo': 'high_income',
    'low_income_typo': 'low_income',
    'lower_middle_income_typo': 'lower_middle_income',
    'upper_middle_income_typo': 'upper_middle_income'
})

print(f"Rows and cols of df2:\n{df2.shape}\n")

## Check the effects of addressing issue 1

print(f"Describe the data after removing and replacing missing values:\n{df2.describe()}\n")
df2_income_groups_unique_vals = df2['income_groups'].unique()
print(f"Unique values in income_groups:\n{df2_income_groups_unique_vals}\n")

## Data distribution
df2_dist = df2.groupby('income_groups').agg({
    'age': ['nunique', 'mean', 'std'],
    'gender': 'nunique',
    'year': 'nunique',
    'population': ['nunique', 'mean', 'std']
}).reset_index()

print(f"df2 distribution by income_groups:\n{df2_dist}\n")
print(f"df2 population mean:\n{df2['population'].mean()}\n")



# Issue 2: Missing Data

## drop missing values from income_groups, gender, and year
df3 = df2.dropna(subset=['income_groups', 'gender', 'year']).copy()

## replace missing values in age with the average age per income_groups value

### calculate the average age for each unique value in income_groups
average_age_by_group = df3.groupby('income_groups')['age'].mean().round() # round to nearest integer

print(f"average age by income_groups:\n{average_age_by_group}\n")

### define a function to replace missing age values with the corresponding average age
def fill_missing_age(row):
    if pd.isnull(row['age']):  # Check if age is NaN or null
        return average_age_by_group[row['income_groups']]  # Return the average age for the income_groups value
    else:
        return row['age']  # If not NaN or null, return the original age

### apply the function to the data to fill missing age values
df3.loc[:, 'age'] = df3.apply(fill_missing_age, axis=1)

## replace missing values in population with the average population for the corresponding year

### calculate the average population for each year
average_population_by_year = df3.groupby('year')['population'].mean().round() # round to nearest integer

print(f"average population by income_groups:\n{average_population_by_year}\n")

### define a function to replace missing age values with the corresponding average age
def fill_missing_population(row):
    if pd.isnull(row['population']):  
        return average_population_by_year[row['year']] 
    else:
        return row['population']

### apply the function to the data to fill missing age values
df3.loc[:, 'population'] = df3.apply(fill_missing_population, axis=1)

print(f"Describe the data after removing and replacing missing values:\n{df3.describe()}\n")
print(f"Check missing values:\n{df3.isna().sum()}\n")

print(f"Rows and cols of df3:\n{df3.shape}\n")

## Data distribution
df3_dist = df3.groupby('income_groups').agg({
    'age': ['nunique', 'mean', 'std'],
    'gender': 'nunique',
    'year': 'nunique',
    'population': ['nunique', 'mean', 'std']
}).reset_index()

print(f"df3 distribution by income_groups:\n{df3_dist}\n")
print(f"population mean d3:\n{df3['population'].mean()}\n")


# Issue 3: Duplicate Data

## remove duplicate rows
df4 = df3.drop_duplicates().copy()
print(f"Describe the data after removing and replacing missing values:\n{df3.describe()}\n")
print(f"Check duplicate rows:\n{df4.duplicated().sum()}\n")
print(f"Rows and cols of df4:\n{df4.shape}\n")

## Data distribution
df4_dist = df4.groupby('income_groups').agg({
    'age': ['nunique', 'mean', 'std'],
    'gender': 'nunique',
    'year': 'nunique',
    'population': ['nunique', 'mean', 'std']
}).reset_index()

print(f"df4 distribution by income_groups:\n{df4_dist}\n")

print(f"df4 description:\n{df4.describe()}\n")

# Identify columns with float64 data type
float_columns = df4.select_dtypes(include='float64').columns

# Convert the identified float columns to integer type
df4[float_columns] = df4[float_columns].astype('int64')

print(f"df4 dtype:\n{df4.dtypes}\n")


## Number of unique values in each column
df4_col_unique_counts = df4.nunique()

## Mean of numerical columns (ignoring NaN values)
df4_mean_values = df4.mean(numeric_only=True)

## Number of non-null values in each column
df4_col_non_null_counts = df4.count()

print(f"df4 number of unique values per column:\n{df4_col_unique_counts}\n")
print(f"df4 mean of columns:\n{df4_mean_values}\n")
print(f"df4 number of non-null values per column:\n{df4_col_non_null_counts}\n")

# File name
file_name = 'cleaned_population_data.csv'

# Check if the file exists in the current directory
if not os.path.isfile(file_name):
    # If it doesn't exist, save the DataFrame as a CSV file
    df4.to_csv(file_name, index=False)
    print(f"{file_name} has been saved.")
else:
    print(f"{file_name} already exists.")