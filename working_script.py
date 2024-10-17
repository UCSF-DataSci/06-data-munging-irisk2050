import pandas as pd
import numpy as np
import tqdm
import argparse
import os
from scipy import stats
import matplotlib

# set working directory
os.chdir("/Users/iriskim/Desktop/06-data-munging-irisk2050")

# load data
df = pd.read_csv("messy_population_data.csv")

# EDA
## Describe data
df_summary = df.describe()

df_info = df.info()

## Number of rows and columns
df_num_rows, df_num_columns = df.shape

## Column names
df_col_names = df.columns.tolist()

## Data types of each column
df_col_data_types = df.dtypes

## Number of missing values in each column (NA, NaN)
df_missing_values = df.isna().sum()
# Find the first row with any missing value
df_first_missing_row = df[df.isna().any(axis=1)].iloc[0]

## Number of unique values in each column
df_col_unique_counts = df.nunique()

## Mean of numerical columns (ignoring NaN values)
mean_values = df.mean(numeric_only=True)

## Number of non-null values in each column
df_col_non_null_counts = df.count()

## Check for duplicates
df_duplicates_count = df.duplicated().sum()
df_first_duplicate = df[df.duplicated()].iloc[0]

## Check for data outliers
df_age_z_scores = np.abs(stats.zscore(df['age'])) 
df_age_outliers = df[df_age_z_scores > 3]

df_gender_z_scores = np.abs(stats.zscore(df['gender'])) 
df_gender_outliers = df[df_gender_z_scores > 3]

df_year_z_scores = np.abs(stats.zscore(df['year'])) 
df_year_outliers = df[df_year_z_scores > 3]

df_population_z_scores = np.abs(stats.zscore(df['population'])) 
df_population_outliers = df[df_population_z_scores > 3]

## Check unique values for income_groups and age
df_income_groups_unique_vals = df['income_groups'].unique()
df_gender_unique_vals = df['gender'].unique()

## Check typos
df_typo_count = (df['income_groups'].str.contains('typo', case=False, na=False)).sum()
df_first_typo_row = df[df['income_groups'].str.contains('typo', case=False, na=False)].iloc[0]

## Data distribution
df_dist = df.groupby('income_groups').agg({
    'age': ['nunique', 'mean', 'std'],
    'gender': 'nunique',
    'year': 'nunique',
    'population': ['nunique', 'mean', 'std']
}).reset_index()

# Print the results
print(f"Data summary:\n{df_summary}\n")
print(f"Data info:\n{df_info}\n")
print(f"Number of rows: {df_num_rows}\n")
print(f"Number of columns: {df_num_columns}\n")
print(f"Column names: {df_col_names}\n")
print(f"Data types of each column:\n{df_col_data_types}\n")
print(f"Missing values in each column:\n{df_missing_values}\n")
print(f"Number of unique values in each column:\n{df_col_unique_counts}\n")
print(f"Mean of each numerical column:\n{mean_values}\n")
print(f"Number of non-null values in each column:\n{df_col_non_null_counts}\n")
print(f"Number of duplicate rows:\n{df_duplicates_count}\n")
print(f"Number of outliers in age column:\n{len(df_age_outliers)}\n")
print(f"Number of outliers in gender column:\n{len(df_gender_outliers)}\n")
print(f"Number of outliers in year column:\n{len(df_year_outliers)}\n")
print(f"Number of outliers in population column:\n{len(df_population_outliers)}\n")
print(f"First row with missing values:\n{df_first_missing_row}\n")
print(f"First duplicate row:\n{df_first_duplicate}\n")
print(f"Unique values of income_group:\n{df_income_groups_unique_vals}\n")
print(f"Unique values of gender:\n{df_gender_unique_vals}\n")
print(f"Unique values of age:\n{df['age'].unique()}\n")
print(f"Number of negative values in population:\n{(df['population'] < 0).sum()}\n")
print(f"Number of negative values in year:\n{(df['year'] < 0).sum()}\n")
print(f"Number of rows with typo in income_groups:\n{df_typo_count}\n")
print(f"First row with typo in income_groups:\n{df_first_typo_row}\n")
print(f"Is age all whole numbers:\n{(df['age'].dropna() % 1 == 0).all()}\n")
print(f"Is gender all whole numbers:\n{(df['gender'].dropna() % 1 == 0).all()}\n")
print(f"Is year all whole numbers:\n{(df['year'].dropna() % 1 == 0).all()}\n")
print(f"Is population all whole numbers:\n{(df['population'].dropna() % 1 == 0).all()}\n")
print(f"Data distribution by income_groups:\n{df_dist}\n")
print(f"Number of population values less than or equal to 500:\n{(df['population'] <= 500).sum()}")