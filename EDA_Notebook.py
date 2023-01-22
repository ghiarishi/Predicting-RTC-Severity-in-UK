import pandas as pd

data = pd.read_csv('accident_data.csv')
data.head()

"""
2. Data Preparation and Cleaning
Load data using pandas
Look at some information about data and contained features
Fixing any missing values
"""

data.shape

"""The dataset contains 1,048,575 records, each with 34 features/columns"""

#Check information about datatype for individual columns
data.info()

#Display the columns/features contained in the data
data.columns

# get statistical summaries for numerical columns
data.describe()

#get count of numberical columns
len(data.describe())

"""#  Check null values"""

percentage_na = data.isna().sum().sort_values(ascending=False)*100/len(data)
percentage_na

#Visualize percentage_na
import seaborn as sns
sns.set_style("darkgrid")
percentage_na[percentage_na>0].plot(kind='barh')

# Drop columns with large number of NAs
columns_to_drop = ['2nd_Road_Class','1st_Road_Class','LSOA_of_Accident_Location']
data.drop(columns=columns_to_drop,inplace=True)

"""# 3. Exploratory Analysis and Visualization
Columns we will analyze:
- Accident Severity
- Date
- Day of the week
- Did Police Attend on Scence
- Latitude
- Light Condition at the time of accident
- Local Authority
- Number of casualties
- Roadway surface condition
- Road type
- Speed limit
- Time
- Urban/Rural
- Weather Condition
- Year
"""

data.columns

columns_to_analyze = ['Accident_Index','Accident_Severity','Date','Day_of_Week','Did_Police_Officer_Attend_Scene_of_Accident','Latitude','Longitude',
                      'Light_Conditions','Local_Authority_(District)','Number_of_Casualties','Road_Surface_Conditions',
                      'Road_Type','Speed_limit','Time','Urban_or_Rural_Area', 'Weather_Conditions','Year']
data_subset = data[columns_to_analyze]

data_subset.head()

"""# Local Authority Analysis."""

data_subset.rename(columns={'Local_Authority_(District)':'authority'},inplace=True)
data_subset.head()

local_authorities = data_subset.authority.unique()
local_authorities

# Get top 20 authorities
local_authorities_by_collisions = data_subset.authority.value_counts(ascending=False)
local_authorities_by_collisions[:20]

local_authorities_by_collisions[:20].plot(kind='bar')

"""- Birmingham has the most number of collisions (21,384).
- The number of collisions per city decreasese exponentially

#  Anayze Accident Severity
"""

severities = data_subset['Accident_Severity']
severity_levels = severities.unique()
severity_levels

severities.isna().sum() # check if there are any null values

severities.value_counts()

#Calculate Percentages 
severities.value_counts()*100/len(severities)

# Visualize the accident severity in histogram
severities.value_counts().plot(kind='bar')

"""# Anayze Date and Time"""

data_subset['Date']

data_subset['Date'].isna().sum()

#Time: 
times = data_subset.Time
times

times.isna().sum()

# drop rows with time null: 
data_subset.dropna(subset=['Time'],inplace=True)

data_subset.Time.isna().sum()

# Create a new datetime columns based on the individual values given

data_subset['DateTime'] = data_subset['Date']+' '+ data_subset['Time']
data_subset.head()

data_subset.DateTime.isna().sum() # make sure the new columns does not contain NA

data_subset['DateTime'] = pd.to_datetime(data_subset['DateTime']) # Convert Datetime to pandas datetime

sns.distplot(data_subset.DateTime.dt.day, bins=31, kde=False, norm_hist=True)
import matplotlib.pyplot as plt

plt.axvline(10.0, 0,color='red')
plt.axvline(13.0, 0,color='red')

"""Most accidents occurs between dates 10 - 13 of the month, on first day of the month and last days of the month number of accidents gets down."""

sns.distplot(data_subset.DateTime.dt.day_of_week, bins=7, kde=False, norm_hist=True)

"""Most accidents occur in Fridays"""

sns.distplot(data_subset.DateTime.dt.month, bins=12, kde=False, norm_hist=True)

"""Accidents occurance trend looks similar throughout the year"""

### Analyze time of occurance of collisions
sns.distplot(data_subset.DateTime.dt.hour, bins=24, kde=False, norm_hist=True)

plt.axvline(8.0, 0,color='red')
plt.axvline(14.0, 0,color='red')
plt.axvline(18.0, 0,color='red')

"""# Analyze response behaviours of police after collisions

"""

data_subset.head()

police_responses = data_subset.Did_Police_Officer_Attend_Scene_of_Accident
police_responses.value_counts()

#calculate police response by percentages
response_percentages = police_responses.value_counts()*100/len(police_responses)
response_percentages

"""- 80.4% of the time police attended to the scene of accident (843,029 collisions)
- 19.3% of the time police did not attend to the scene of the accidents -(202112) - WHY? - Could the severity matter?
- 0.3% (3066) of the collisions were reported through self-completion form (No police were needed)

# Analyze the 19.2% accidents where police did not attend.
"""

collisions_with_no_police_attendance = data_subset[data_subset['Did_Police_Officer_Attend_Scene_of_Accident']==2]
len(collisions_with_no_police_attendance)

collisions_with_no_police_attendance.Accident_Severity.value_counts()

# Calculate percentages
collisions_with_no_police_attendance.Accident_Severity.value_counts()*100/len(collisions_with_no_police_attendance)

"""- Probabably the police did not attend because the severity of the collision was slight.
- But there are 195 fatal collisions where the police did not attend WHY? - Further analysis is required

# Analyze location of collisions:
"""

import folium
from folium.plugins import HeatMap,FastMarkerCluster

data_subset.Latitude

data_subset.Latitude.isna().sum()

data_subset['Longitude'] = data['Longitude']

data_subset.Longitude.isna().sum()

data_subset.dropna(subset=['Longitude'],inplace=True)

data_subset.Latitude.isna().sum()

data_subset.Longitude.isna().sum()

sample_data = data_subset.sample(int(0.001 * len(data_subset)))
lat_lon_pairs = list(zip(list(sample_data.Latitude), list(sample_data.Longitude)))

map = folium.Map()
# HeatMap(lat_lon_pairs).add_to(map)
FastMarkerCluster(lat_lon_pairs).add_to(map)

map

"""# Analyze number of casualties"""

casualties=data_subset.Number_of_Casualties
casualties
sns.histplot(casualties,log_scale=True)

casualties.value_counts()

#Calculate percentages
casualties.value_counts()*100/len(casualties)

"""- More than 92% of the accidents involved casualties invloving less than 2 people. 
- 8 percent of the accidents involved large number of casualties ranging from 4 to 43.
"""

#get high casualty accidents: 
high_casualty = data_subset[data_subset.Number_of_Casualties>5]
high_casualty.head()

# when do these high casualty collisions occur happen? 
sns.distplot(high_casualty.DateTime.dt.hour, bins=24, kde=False, norm_hist=True)
import matplotlib.pyplot as plt

plt.axvline(13.0, 0,color='red')
plt.axvline(18.0, 0,color='red')

# Local authorities where these high casualty accidents happens
local_authorities_by_high_collisions = high_casualty.authority.value_counts(ascending=False)
local_authorities_by_high_collisions[:20]

"""# 4. Question to Answer
- What is the distribution of severity of injuries across the country?  (ANSWERED)
- Which days do most accidents occur? (ANSWERED)
- What is the response behaviour of police when accidents occur? Is it affected by the severity of the accidents?
  - But there are 195 fatal collisions where the police did not attend WHY??

- Where do most accidents occur? (ANSWERED with MAP)
- What are the top 20 Local authorities with most collisions. (ANSWERED)
- What is the trend of number of casualties?(ANSWERED)

# 5. Summary and Conclusion
- 85% (895,883) of the reported accidents resulted were slightly severe, while 13% (138,192) of the accidents were serious, 1.4% (14,500) were fatal accidents


- Accidents occurance looks similar throughout the year

- Peak collision happens around 8 in the morning and during the day between 14 - 18, the rate goes down after 18.

-  Probabably the police did not attend because the severity of the collision was slight (94% of collisions where police did not attend has slight severity)

- Police did not attend in 195 fatal collisions - More explanation is needed here!


- Birmingham has the most number of collisions (21,384).
- The number of collisions per city decreasese exponentially

- More than 92% of the accidents involved casualties invloving less than 2 people. 

- 8 percent of the accidents involved large number of casualties ranging from 4 to 43 - there are more accidents happening.

- Most high casualty accidents occurs during the day between 12 - 18
"""



