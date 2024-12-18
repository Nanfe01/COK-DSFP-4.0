#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import seaborn as sns


# In[8]:


import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# In[9]:


vaccination_pop = pd.read_csv('distribution-of-covid-19-fully-vaccinated-population-in-nigeria.csv')
vaccination_doses = pd.read_csv('astrazeneca-and-moderna-vaccination-doses-by-state.csv')
shopify = pd.read_csv('shopify_data_seller2.csv')
covid_19 = pd.read_excel('nga_subnational_covid19.xlsx')


# In[5]:


df=[covid_19, vaccination_doses, vaccination_pop, shopify]


# # Covid_19

# In[6]:


covid_19.head()


# In[7]:


covid_19.columns


# In[8]:


covid_19.rename(columns = {
    'ID': 'ID',
    'DATE': 'DATE',
    'ISO_3': 'ISO_3',
    'PAYS': 'COUNTRY',
    'ID_PAYS': 'COUNTRY_ID',
    'REGION': 'REGION',
    'ID_REGION': 'REGION_ID',
    'CONTAMINES': 'CONFIRMED',
    'DECES': 'DEATHS',
    'GUERIS': 'RECOVERED',
    'CONTAMINES_FEMME': 'CONFIRMED_FEMALE',
    'CONTAMINES_HOMME': 'CONFIRMED_MALE',
    'CONTAMINES_GENRE_NON_SPECIFIE': 'CONFIRMED_GENDER_UNSPECIFIED',
    'SOURCE': 'SOURCE'
}, inplace = True)


# In[9]:


covid_19.columns


# In[10]:


covid_19.head()


# In[11]:


# To keep only needed columns

new_covid = covid_19.drop(columns=['ID', 'DATE', 'ISO_3', 'COUNTRY', 'COUNTRY_ID', 'REGION_ID', 'SOURCE'])  


# In[12]:


new_covid.head()


# In[13]:


# Filling null values with 0
new_covid.fillna(0, inplace=True)
new_covid['REGION'] = new_covid['REGION'].replace('Federal Capital Territory', 'FCT')


# ## Objective 1
# To find the top ten states by death rate

# In[14]:


# Top ten states with highest death rates
death_covid = new_covid.groupby('REGION')['DEATHS'].sum().reset_index()
death_covid.head()


# In[114]:


# Sort and select top 10
death_top10 = death_top10.sort_values(by='DEATHS', ascending=False).head(10)
print(death_top10)


# In[16]:


# Creating a bar chart using plt
plt.bar(death_top10['REGION'], death_top10['DEATHS'], color ='Blue')
plt.title('Top 10 States with Highest Deaths')
plt.xlabel('Number of Deaths')
plt.xticks(rotation=45)
plt.ylabel('States')
plt.figure(figsize=(18, 10)
plt.show()


# In[17]:


# Creating a horizontal bar chart using sns
sns.barplot(x='DEATHS', y='REGION', data= death_top10, color = 'r')
plt.title('Top 10 States with Highest Deaths')
plt.xlabel('Number of Deaths')
plt.ylabel('States')
plt.show()


# In[18]:


# Creating a bar chart using px
fig = px.bar(death_top10, x='REGION', y='DEATHS', color='DEATHS',
             color_continuous_scale='Reds', title='Top 10 States with Highest Deaths')
fig.update_layout(xaxis={'categoryorder': 'total descending'}) 
fig.show()


# ## Objectives 2
# 
# Top 10 States with highest recovery rates
# 

# In[53]:


# Calculate the recovery rate
state_totals = new_covid.groupby('REGION')[['CONFIRMED', 'RECOVERED']].sum().reset_index('REGION')
state_totals['Recovery Rate (%)'] = round((state_totals['RECOVERED'] / state_totals['CONFIRMED']) * 100, 2)
state_totals. head()
state_totals.columns


# In[54]:


# Sort and select top 10
recovery_top10 = state_totals.sort_values(by='Recovery Rate (%)', ascending=False).head(10)
recovery_top10.set_index('REGION', inplace=True)
print(recovery_top10)


# In[58]:


# Creating a bar chart using plt
plt.bar(recovery_top10.index, recovery_top10['Recovery Rate (%)'], color ='Green')
plt.title('Top 10 States with Highest Recovery Rate(%)')
plt.xlabel('Recovery Rate (%)')
plt.xticks(rotation=45)
plt.ylabel('States')
plt.figure(figsize=(18, 10))
plt.show()



# # SHOPIFY

# In[ ]:


shopify.head()


# In[ ]:


shopify.columns


# In[ ]:


shopify.dtypes


# ## Objective 1
# Conversion Rate by Referrer Source

# In[12]:


#(Calculate, Conversion, Rate, by, Referrer, source)

shopify['conversion_rate'] = (shopify['total_orders_placed'] / shopify['total_sessions']) * 100
conversion_by_referrer = shopify.groupby('referrer_source')['conversion_rate'].mean()
print(conversion_by_referrer)


# In[13]:


# Visualize conversion rate by referrer_source
fig = px.bar(shopify,
             x='referrer_source',
             y='conversion_rate',
             color='referrer_source',
             title='Conversion Rate by Referrer Source',
             labels={'conversion_rate': 'Conversion Rate (%)', 'referrer_source': 'Referrer Source'})
fig.show()


# ## Objective 2
# 
# Bounce rate by OS

# In[14]:


# Group by 'ua_os' to identify OS-specific bounce rates
bounce_by_os = shopify.groupby('ua_os')['total_bounce_rate'].mean()
print("Average Bounce Rate by OS:", bounce_by_os)


# In[45]:


# Visualize bounce rate by ua_os
plt.figure(figsize=(8, 6))
sns.barplot(data=shopify, x='ua_os', y='total_bounce_rate', hue='ua_os' , ci=None)
plt.title('Bounce Rate by Operating System')
plt.xlabel('Operating System')
plt.ylabel('Bounce Rate (%)')
plt.show()



# ## Objective 3
# 
# Conversion Rate, Orders and Page Views by Form Factor

# In[16]:


# Calculate Conversion Rate (orders / sessions)

shopify['conversion_rate'] = (shopify['total_orders_placed'] / shopify['total_sessions']) * 100
shopify_grouped = shopify.groupby('ua_form_factor').agg({
    'total_orders_placed': 'sum',
    'total_pageviews': 'sum',
    'conversion_rate': 'mean'
}).reset_index()

# Print the grouped data
print(shopify_grouped)


# In[17]:


# Visualize total orders placed by form factor
fig = px.bar(shopify_grouped,
             x='ua_form_factor',
             y='total_orders_placed',
             color='ua_form_factor',
             title='Total Orders Placed by Form Factor',
             labels={'total_orders_placed': 'Total Orders', 'ua_form_factor': 'Form Factor'})
fig.show()



# In[18]:


# Visualize total pageviews by form factor
fig = px.bar(shopify_grouped,
             x='ua_form_factor',
             y='total_pageviews',
             color='ua_form_factor',
             title='Total Pageviews by Form Factor',
             labels={'total_pageviews': 'Total Pageviews', 'ua_form_factor': 'Form Factor'})
fig.show()



# In[19]:


# Visualize conversion rate by form factor
fig = px.bar(shopify_grouped,
             x='ua_form_factor',
             y='conversion_rate',
             color='ua_form_factor',
             title='Conversion Rate by Form Factor',
             labels={'conversion_rate': 'Conversion Rate (%)', 'ua_form_factor': 'Form Factor'})
fig.show()


# # VACCINATION POPULATION

# In[20]:


vaccination_pop. head()


# In[21]:


# Renaming and viewing Column Headers
vaccination_pop = vaccination_pop.rename(columns={'Region': 'State'})
vaccination_pop.columns


# In[22]:


vaccination_pop.dtypes


# In[23]:


vaccination_pop['Population'] = vaccination_pop['Population'].replace({',': '', ' ': ''}, regex=True)
vaccination_pop['First Dose (Partially Vaccinated)'] = vaccination_pop['First Dose (Partially Vaccinated)'].replace({',': '', ' ': ''}, regex=True)
vaccination_pop['Second Dose (Fully Vaccinated)'] = vaccination_pop['Second Dose (Fully Vaccinated)'].replace({',': '', ' ': ''}, regex=True)


# In[24]:


vaccination_pop['Population'] = pd.to_numeric(vaccination_pop['Population'], errors='coerce')
vaccination_pop['First Dose (Partially Vaccinated)'] = pd.to_numeric(vaccination_pop['First Dose (Partially Vaccinated)'], errors='coerce')
vaccination_pop['Second Dose (Fully Vaccinated)'] = pd.to_numeric(vaccination_pop['Second Dose (Fully Vaccinated)'], errors='coerce')
print(vaccination_pop.dtypes)


# In[25]:


# Assigning Geopolitical zones to the states

def assign_zone(state):
    north_central = ['Benue', 'Kogi', 'Kwara', 'Nasarawa', 'Niger', 'Plateau', 'FCT']
    north_east = ['Adamawa', 'Bauchi', 'Borno', 'Gombe', 'Taraba', 'Yobe']
    north_west = ['Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Sokoto', 'Zamfara']
    south_east = ['Abia', 'Anambra', 'Ebonyi', 'Enugu', 'Imo']
    south_south = ['Akwa Ibom', 'Bayelsa', 'Cross River', 'Delta', 'Edo', 'Rivers']
    south_west = ['Ekiti', 'Lagos', 'Ogun', 'Ondo', 'Osun', 'Oyo']
    
    if state in north_central:
        return 'North-Central'
    elif state in north_east:
        return 'North-East'
    elif state in north_west:
        return 'North-West'
    elif state in south_east:
        return 'South-East'
    elif state in south_south:
        return 'South-South'
    elif state in south_west:
        return 'South-West'
    else:
        return 'Unknown'  


# In[26]:


vaccination_pop['Geopolitical Zone'] = vaccination_pop['State'].apply(assign_zone)
vaccination_pop.head()


# ## Objective 1
# 
# Identifying the states with the lowest Vaccination rates

# In[27]:


# Calculating the Vaccination Rates accross States

def calc_vaccination_rate(group):
    group['Vaccination Rate'] = (group['Total Vaccinated Population'] / group['Population'])* 100
    return group

state_vacc_rate = vaccination_pop.groupby('State').apply(calc_vaccination_rate)
print(state_vacc_rate.head())
state_vacc_rate.columns


# In[28]:


# Ranking the least 5
state_vacc_rate10 = state_vacc_rate.sort_values(by='Vaccination Rate').head(5)
print(state_vacc_rate10)


# In[29]:


# Visualizing with plt

plt.figure(figsize=(10, 8))
plt.bar(state_vacc_rate10['State'], state_vacc_rate10['Vaccination Rate'], color='skyblue')
plt.xlabel('Vaccination Rate')
plt.ylabel('State')
plt.title('States with Lowest Vaccination Rates (%)')
plt.show()



# ## Objective 2
# 
# Vaccination Rates Amongst Geopolitical zones

# In[30]:


# Summing the population and Total Vaccinated Population y Geopolitical Zones

zone_vacc = vaccination_pop.groupby('Geopolitical Zone')[['Population', 'Total Vaccinated Population']].sum()
zone_vacc.head()


# In[31]:


# Vaccination Rates by Geopolitical Zones

zone_vacc['Vaccination Rate'] = ((zone_vacc['Total Vaccinated Population'] / zone_vacc['Population']) *100)
print(zone_vacc.head())


# In[32]:


fig = px.bar(zone_vacc,
             x=zone_vacc.index,
             y='Vaccination Rate',
             title='Vaccination Rate by Geopolitical Zone',
             labels={'Vaccination Rate': 'Vaccination Rate', 'Geopolitical Zone': 'Zone'},
             color='Vaccination Rate',
             color_continuous_scale='Viridis')
fig.show()


# ## Objective 3
# 
# Vaccination drop-off rate

# In[33]:


# Calculate Drop-off Rate

vaccination_pop['Drop-off Rate'] = ((vaccination_pop['First Dose (Partially Vaccinated)'] - vaccination_pop['Second Dose (Fully Vaccinated)']) / 
                                      vaccination_pop['First Dose (Partially Vaccinated)']) * 100
print(vaccination_pop[['State', 'Drop-off Rate']])


# In[34]:


# Categorization

def categorize_drop_off(rate):
    if rate >= 80:
        return 'Extreme'
    elif rate >= 50:
        return 'Very High'
    elif rate >= 35:
        return 'High'
    elif rate >= 20:
        return 'Fair'
    else:
        return 'Good'

vaccination_pop['Category'] = vaccination_pop['Drop-off Rate'].apply(categorize_drop_off)
print(vaccination_pop[['State', 'Drop-off Rate', 'Category']])


# In[35]:


# Create a bar chart to visualize the categories of drop-off rates

fig = px.bar(vaccination_pop,
             x='State',
             y='Drop-off Rate',
             color='Category',
             title='Vaccination Drop-off Rate Categories by State',
             labels={'Drop-off Rate': 'Drop-off Rate (%)', 'State': 'State', 'Category': 'Category'},
             color_discrete_map={'Extreme': 'white', 'Very High': 'red', 'High': 'orange', 'Fair': 'yellow', 'Good': 'green'})

fig.show()


# # DOSES

# In[36]:


vaccination_doses.head()


# In[37]:


print(vaccination_doses)
vaccination_doses.columns


# ## Objective 1
# 
# Completion Rates for AstraZeneca

# In[38]:


vaccination_doses['AstraZeneca (First dose)'] = vaccination_doses['AstraZeneca (First dose)'].replace({',': '', ' ': ''}, regex=True)
vaccination_doses['AstraZeneca (Second dose)'] = vaccination_doses['AstraZeneca (Second dose)'].replace({',': '', ' ': ''}, regex=True)
vaccination_doses['AstraZeneca (First dose)'] = pd.to_numeric(vaccination_doses['AstraZeneca (First dose)'], errors='coerce')
vaccination_doses['AstraZeneca (Second dose)'] = pd.to_numeric(vaccination_doses['AstraZeneca (Second dose)'], errors='coerce')
vaccination_doses['Moderna (First Dose)'] = pd.to_numeric(vaccination_doses['Moderna (First Dose)'], errors='coerce')

print(vaccination_doses)


# In[39]:


# AstraZeneca completion rate

vaccination_doses['AstraZeneca Completion Rate (%)'] = (vaccination_doses['AstraZeneca (Second dose)'] / vaccination_doses['AstraZeneca (First dose)']) * 100


# In[40]:


# Visualize completion rates
fig = px.bar(
    vaccination_doses,
    x='State',
    y='AstraZeneca Completion Rate (%)',
    title='AstraZeneca Vaccination Completion Rates by State',
    labels={'AstraZeneca Completion Rate (%)': 'Completion Rate (%)'},
    color='AstraZeneca Completion Rate (%)',
    color_continuous_scale='Blues'
)
fig.show()


# ## Objective 2
# 
# Comparison of first doses of both Vaccines

# In[41]:


# Transform data for grouped bar chart
vaccination_doses_long = vaccination_doses.melt(
    id_vars='State',
    value_vars=['AstraZeneca (First dose)', 'Moderna (First Dose)'],
    var_name='Vaccine Type',
    value_name='First Dose Count'
)

# Visualize grouped bar chart
fig = px.bar(
    vaccination_doses_long,
    x='State',
    y='First Dose Count',
    color='Vaccine Type',
    barmode='group',
    title='First Dose Distribution by Vaccine Type and State',
    labels={'First Dose Count': 'Number of First Doses'}
)
fig.show()


# In[46]:


data_types= shopify.dtypes


# In[ ]:





# In[ ]:




