#!/usr/bin/env python
# coding: utf-8

# In[9]:


get_ipython().run_line_magic('matplotlib', 'inline')
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import os

# File to Load (Remember to change these)
city_data_to_load = "data/city_data.csv"
ride_data_to_load = "data/ride_data.csv"

# Read the City and Ride Data
citydata = pd.read_csv(city_data_to_load)
ridedata = pd.read_csv(ride_data_to_load)

citydata.head()
ridedata.head()

citydata = citydata.drop_duplicates('city', keep = 'first')

# Combine the data into a single dataset
combined_data = pd.merge(citydata, ridedata, how="outer", on="city")

# Display the data table for preview
combined_data.head()


# In[11]:


city_group = combined_data.groupby(['city','type'])

fare = city_group['fare'].mean()
rides = city_group['ride_id'].count()
drivers = city_group['driver_count'].mean() 

plt_df = pd.DataFrame({"Average Fare ($)": fare,
          "Total Number of Rides per City": rides,
          "Driver Count": drivers})


plt_df = plt_df.reset_index(level='type')

plt_df = plt_df.rename(columns={"type": "City Types"})


# In[18]:


sns.set(font_scale=1.25)

col_list = ["lightskyblue", "gold", "lightcoral"]

b_plot = sns.lmplot(x='Total Number of Rides per City', y='Average Fare ($)', data=plt_df, fit_reg=False, 
                   scatter_kws={'s':(plt_df['Driver Count'] * 10), 'alpha':1, 'linewidths':1, 'edgecolor':'k'}, 
                   legend_out=False, palette=dict(Suburban=col_list[0], Rural=col_list[1], Urban=col_list[2]),
                   hue='City Types', height=7, aspect=1.30)

plt.show()


# In[3]:


# Show plot
plt.show()


# ## Total Fares by City Type

# In[27]:


type_df = combined_data.groupby(['type'])

fare_totals = type_df['fare'].sum()

explode = (0, 0, 0.1)
plt.pie(fare_totals, explode=explode, labels=type_df.groups, colors=col_list, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title("% of Total Fares by City Type")
plt.show()


# ## Total Rides by City Type

# In[25]:


total_rides = type_df['ride_id'].count()
explode = (0, 0, 0.1)
plt.pie(total_rides, explode=explode, labels=type_df.groups, colors=col_list, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title("% of Total Rides by City Type")
plt.show()


# In[23]:


# Show Figure
plt.show()


# ## Total Drivers by City Type

# In[28]:


unique_df = combined_data.drop_duplicates(['city'], keep='first')
total_drivers = unique_df.groupby('type').sum()['driver_count']

explode = (0, 0, 0.1)
plt.pie(total_drivers, explode=explode, labels=type_df.groups, colors=col_list, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title("% of Total Drivers by City Type")
plt.show()

