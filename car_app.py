"""Used car explorer app"""

import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')  #reading the csv file

# filling the missing values in 'model_year' column using median and grouping by model
df['model_year'] = df['model_year'].astype(float)  # Convert to numerical type
df['model_year'] = df['model_year'].fillna(df.groupby('model')['model_year'].transform('median'))

# filling the missing values in 'cylinders' column using median and grouping by model
df['cylinders'] = df['cylinders'].fillna(df.groupby('model')['cylinders'].transform('median'))

# filling the missing values in 'odometer' column using median and grouping by model
df['odometer'] = df['odometer'].fillna(df.groupby('model')['odometer'].transform('median'))

columns_to_replace = ['paint_color', 'is_4wd']

for column in columns_to_replace:
    df[column] = df[column].fillna('unknown')

st.title('Used cars properties')
st.subheader('Explore the properties of a used cars!')

st.image('image.jpg')

st.header('Get familiar with the used cars data:')

st.dataframe(df)

df['manufacturer'] = df['model'].str.extract(r'(\b\w+)') #getting the column with manufacturer

st.header('Vehicle models by year and condition:')

best = st.checkbox('The best condition cars')

if best: #if else for checkbox
    df=df[df.condition == 'new']
else:
    df=df

fig = px.scatter(df, x="model_year", y="condition", color="model") #condition scatterplot
st.plotly_chart(fig)

data_price = st.header('Check the average cars price by manufacturer:')

avg_price = px.histogram(df, x='manufacturer',
                         y="price", histfunc='avg',
                         color='manufacturer') #avg price histogram
st.plotly_chart(avg_price)

select = st.header('Celect the car by your preferences:')

fuel_select = st.selectbox(
   "Select the fuel type:",
   df['fuel'].apply(lambda x: x.split()[0]).unique(),
   index=None,
   placeholder="Fuel type",
)

transmission_select = st.selectbox(
   "Select the transmission type:",
   df['transmission'].apply(lambda x: x.split()[0]).unique(),
   index=None,
   placeholder="Transmission type",
)

type_select = st.selectbox(
   "Select the car type:",
   df['type'].apply(lambda x: x.split()[0]).unique(),
   index=None,
   placeholder="Car type",
)

prefs = df[(df['fuel'] == fuel_select) &
           (df['transmission'] == transmission_select) &
           (df['type'] == type_select)]

st.dataframe(prefs)
