# Data Cleaning Project: Population Dataset

## 1. Initial State Analysis

### Dataset Overview
- **Name**: messy_population_data.csv
- **Rows**: 125718
- **Columns**: 5

### Column Details
| Column Name   | Data Type  | Non-Null Count | Unique Values |  Mean    |
|---------------|----------- |----------------|---------------|----------|
| income_groups | object     | 119412         | 8             | --       |
| age           | float64    | 119495         | 101           | 50       |
| gender        | float64    | 119811         | 3             | 1.58     |
| year          | float64    | 119516         | 169           | 2025     |
| population    | float64    | 119378         | 114925        | 11298300 |

NOTE 1: income_groups is not numerical, so there is no mean.
NOTE 2: While gender is numerical, the mean has little meaning since the numbers represent categorical data, not quantitative.

### Identified Issues

1. **[Missing Values]**
   - Description: The data has missing values in every column. 
     - income_groups: 6306
     - age: 6223
     - gendeer: 5907
     - year:6202
     - population: 6340
   - Affected Column(s): income_groups, age, gender, year, popluation
   - Example:
     - income_groups: high_income
     - age: NaN
     - gender: 3
     - year: 1960
     - population: 8172589
   - Potential Impact: Missing data can affect analysis if the missingness is not at random. If the missingness if not at random, it can introduce bias into the analysis. For example, if people in higher income groups are less likely to report their age, analysis excluding those responses might show false results that those have higher income are older/younger than they actually are, leading to incorrect conclusions. Additionally, it can cause overfitting or underfitting when training models.

2. **[Duplicate Values]**
   - Description: There are 2950 rows in the data that are duplicates.
   - Affected Column(s): income_groups, age, gender, year, population
   - Example:
     - income_groups: high_income
     - age: 11
     - gender: 1
     - year: NaN
     - population: NaN
   - Potential Impact: Duplicate rows can introduce bias into analysis if certain observations are overrepresented in the data. For example, if the same data point is counted multiple times, it can skew averages, totals, and other summary statistics, leading to misleading conclusions. It can also lead to overfitting in model training.

3. **[Invalid Values]**
   - Description: There are 5959 rows that have an invalid income_groups value. There are 4 invalid income_groups values:
     - high_income_typo
     - low_income_typo
     - lower_middle_income_typo
     - upper_middle_income_typo
   - Affected Column(s): income_groups
   - Example:
     - income_groups: high_income_typo
     - age: 0
     - gender: 1
     - year: 1991
     - population: 7135453
   - Potential Impact:  Invalid values can distort calculations and statistical summaries (e.g., means, medians, variances). For example, an out-of-range value (e.g., age = -1 or 999) included in calculations can drastically affect summary statistics, leading to incorrect interpretations of the data. It can also introduce bias into statistical models and visualizations, making trends or relationships appear incorrectly.

## 2. Data Cleaning Process

### Issue 1: Invalid Values
- **Cleaning Method**: The column income_groups had 4 invalid values which could be replaced with their corresponding valid values:
    - high_income_typo ---------> high_income
    - low_income_typo ----------> low_income
    - lower_middle_income_typo -> lower_middle_income
    - upper_middle_income_typo -> upper_middle_income
- **Implementation**:
  ```python
  ## Replace the invalid values of income_groups with their corresponding valid values
  df['income_groups'] = df['income_groups'].replace({'high_income_typo': 'high_income',
      'low_income_typo': 'low_income',
      'lower_middle_income_typo': 'lower_middle_income',
      'upper_middle_income_typo': 'upper_middle_income'
  })
  ```
- **Justification**: I chose the replacement method because in this case, it was very clear by the invalid values which corresponding valid value it could be replaced with. There was no guesswork, and I was not falsely making up data. I assumed that removing the 'typo' would categorize the rows into their correct groups.
- **Impact**: 
  - Rows affected: 5959
  - Data distribution change: The number of unique values in income_groups went from 9 to 5 after removing all invalid values (any value containing 'typo'). With the invalid values removed, there has been little change in the distribution of data by income_groups. For example, the number of unique year values for value low_income increased from 165 to 166. Also, the average age for high_income increased from 49.94 to 49.97.

### Issue 2: Missing Values
- **Cleaning Method**: I assessed how to handle missing values in the data column by column. 
  - income_groups
    - Removed missing values.
  - age
    - Replaced missing values with the average age for the corresponding income_groups value.
  - gender
    - Removed missing values.
  - year
    - Removed missing values.
  - population
    - Replaced missing values with the average population for the corresponding year.
- **Implementation**:
  ```python
  ## drop missing values from income_groups, gender, and year
  df = df.dropna(subset=['column_name', 'gender', 'year'])

  ## replace missing values in age with the average age per income_groups value

  ### calculate the average age for each unique value in income_groups
  average_age_by_group = df.groupby('income_groups')['age'].mean().round() # round to nearest integer

  ### define a function to replace missing age values with the corresponding average age
  def fill_missing_age(row):
      if pd.isnull(row['age']):  # Check if age is NaN or null
          return average_age_by_group[row['income_groups']]  # Return the average age for the income_groups value
      else:
          return row['age']  # If not NaN or null, return the original age

  ### apply the function to the data to fill missing age values
  df['age'] = df.apply(fill_missing_age, axis=1)

  ## replace missing values in population with the average population for the corresponding year

  ### calculate the average population for each year
  average_population_by_year = df2.groupby('year')['population'].mean().round() # round to nearest integer

  ### define a function to replace missing age values with the corresponding average age
  def fill_missing_population(row):
      if pd.isnull(row['population']):  
          return average_population_by_year[row['year']] 
      else:
          return row['population']

  ### apply the function to the data to fill missing age values
  df['population'] = df.apply(fill_missing_population, axis=1)
  ```
- **Justification**: I chose these methods for several reasons. I chose to drop missing values in income_groups, gender, and year because those were not easily predictable. There was nothing I could use from the remaining information in the row to infer what the missing value could be without risking introducing bias. Additionally, the variables were qualitative - average income_groups, average gender, and average year has no meaning. For age and popualation, these were quantitative variables. Because of this, I felt comfortable using statistics to extrapolate missing values. I didn't wnat to remove them because my data would shrink in size, and so to preserve my sample size while being conscious of bias, I chose to replace the missing values with the average age (per income_groups) and average population (per year). I chose these reference groups because age changes predictably with year (increment by 1), and thus wouldn't be useful. However, the average age per income_groups value could vary (e.g. high_income could be associated with higher average age, since the person has had more time to accumulate wealth and assets). I thought age would be more closely captured by income_groups, which is why I conditioned the average on that column. Similarly for population, I conditioned it on year, since the population changes year over year as people are born and die. I assumed that this population figure represented the overall population, and not the population of each income_groups value.
- **Impact**: 
  - Rows affected: 17543
  - Data distribution change: After addressing the missing values, there were some slight changes in the distribution of the data. The average population decreased from 1.112983e+08 to 1.108945e+08. Looking at the data aggregated by income_groups, there were also changes. For high_income, the number of unique population values dropped from 26269 to 25060. However, the average population for high_income increased from 6.870735e+07 to 7.011342e+07. For lower_middle_income, the number of unique population values decreased from 26087 to 25034 and the average population also decreased from 1.925412e+08 to 1.812189e+08.

### Issue 3: Duplicate Values
- **Cleaning Method**: Remove all duplicate rows.
- **Implementation**:
  ```python
  # Include relevant code snippet
  df = df.drop_duplicates()
  ```
- **Justification**: I chose to remove all duplicate rows because I didn't want my data to overweight certain values. Duplicate data can artificially inflate the size of certain categories, leading to incorrect conclusions. For example, if the same observation appears multiple times, it may skew results in favor of that repeated observation. Since duplicates can affect the calculation of summary statistics, I chose to remove so that I could avoid misleading insights, especially when aggregating or summarizing data. I assumed that the rows did not represent unique individuals; if it had, then duplicates would be allowed, since it's possible for multiple people to be of the same age, same income group, in the same year with the same population size.
- **Impact**: 
  - Rows affected: 2717
  - Data distribution change: The 25th percentile for age increased from 25 to 26. The 75th percentile for age decreased from 75 to 74. The average population increased from 1.112983e+08 to 1.133614e+08. Across all income_groups values, the number of unique population values decreased. For high_income, the average population increased from 6.870735e+07 to 7.167433e+07. The number of unique ages across income_groups values stayed the same.



## 3. Final State Analysis

### Dataset Overview
- **Name**: cleaned_population_data.csv (or whatever you named it)
- **Rows**: 105458
- **Columns**: 5

### Column Details
| Column Name   | Data Type  | Non-Null Count | Unique Values |  Mean     |
|---------------|----------- |----------------|---------------|-----------|
| income_groups | object     | 119412         | 4             | --        |
| age           | int64      | 119495         | 101           | 50        |
| gender        | int64      | 119811         | 3             | 1.58      |
| year          | int64      | 119516         | 169           | 2025      |
| population    | int64      | 119378         | 99183         | 113361400 |

### Summary of Changes
- [List major changes made to the dataset]
  - Replaced invalid values including 'typo' from the column income_groups with their corresponding valid values.
  - Removed rows missing income_groups information.
  - Replaced missing age values with the average age for each row's income_groups value.
  - Removed rows missing gender and year information.
  - Replaced missing population values with the average population for each row's year value.
  - Removed duplicate rows.
- [Discuss any significant changes in data distribution]
  - The number of unique values in each column either stayed the same (gender kept 3 unique values) or decreased (income_groups went from 8 (not including NaN) to 4).
  - The average population increased from 1.112983e+08 to 1.133614e+08. The average age increased slightly from 50.007038 to 50.032895. The stanard deviation for age decreased from 29.15 to 28.44. The min and max of the values stayed the same across age, gender, year, and population. There wasn't much change in the data distribution.

### Reflection
1. Describe your cleaned dataset and how it compares to the original dirty one.
   - There are no more missing values, no duplicate rows, and fewer rows. 
   - The cleaned data set only contains valid values (removed invalid categories containing 'typo' in income_groups and verified that age, gender, year, and population were non-negative integers).
   - Data distribution-wise, there were few differences between the cleaned and dirty. The greatest change was in the average population size. 
   - The cleaned data set had fewer unique values in some columns.
2. Discuss any challenges faced and how you overcame them.
   - I had challenges figuring out what to look at for data validation. I researched online, and found ways to consider data outliers (extreme values in the data that may skew summary statistics) and also data interpretation (using outside knowledge to know that age cannot be negative, so checking to see if there are any negative ages). This took some creativity, but once I found a couple examples, the rest became clear.
   - Difficulty deciding on the order of addressing issues. I initially addressed the duplicate rows first, before realizing that I needed to take of missing values and replacing invalid values first, because afterwards I could get duplicate rows again with my new cleaned data. Figuring out the order to address data issues was important.
3. Reflect on what you learned from this process.
   - I learned examples of data validation, and how to use outside knowledge to identify valid and invalid values in data. 
   - I learned to modify my dataframe column data types, so as to prevent future data entry errors (e.g., I changed year to an int64 instead of a float64 data type).
   - I learned to examine the order in which I address data issues so as to avoid repetition.
4. Suggest potential next steps or further improvements.
   - Next steps would me to visualize or model the data. While I used averages in my data replacements, averages are susceptible to skewedness. I would want to plot the data first to examine whether it is normal, then decide on whether to replace missing values with the mean or the median.
   - I would want to do further data validation checks. Upon examining the data, there were 463 rows where the population value was <= 500. I assumed that the population data was for the U.S. or some other large country; given this info, it is highly suspect that the population size is so small. I would want to do further investigation into whether these values are valid or are mistakes.
   - Similarly, I want to investigate year. Some years are into the future. I'd like to know if this is predictive data, or if the years were entered in incorrectly.