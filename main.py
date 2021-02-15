import streamlit as st
import pandas as pd 
from streamlit_folium import folium_static
import folium

st.title("World Airports Locator App")

@st.cache # read data from csv
def load_data():
    # df = pd.read_csv("world_airports.csv") 
    df = pd.read_csv("world_airports.csv", usecols = ['name','latitude_deg', 'longitude_deg', 'iso_country', 'iso_region', 'municipality'])
    # remove unnecessary columns
    # df = df.drop(columns=['continent', 'gps_code', 'iata_code', 'home_link', 'wikipedia_link', 'keywords'])
    return df

df = load_data()

# number of all airports
st.header("Total Number of all Airports:")
index = df.index
number_of_rows = len(index)
st.write(number_of_rows)

@st.cache # use cache to load faster
def loadCountry():
    country = df["iso_country"].unique()
    return country

countries = st.sidebar.selectbox("Select Country: ", loadCountry())

@st.cache
def loadState():
    count = df.loc[(df['iso_country'] == countries)]
    state = count['iso_region'].unique()
    # state = [e[3:] for e in state] # clean data here
    return state

states = st.sidebar.selectbox("Select State: ", loadState())

@st.cache
def loadCity():
    loc = df.loc[(df['iso_country'] == countries) & (df['iso_region'] == states)]
    city = loc['municipality'].unique()
    return city

city = st.sidebar.selectbox("Select City: ", loadCity())

@st.cache
def loadData():
    loc = df.loc[(df['iso_country'] == countries) & (df['iso_region'] == states) & (df['municipality'] == city)]
    return loc

# Display dataframe
data = loadData()
st.dataframe(data)

#
index1 = data.index
rows = len(index1)
st.header("Number of Airports:")
st.write(city)
st.write(rows)

m = folium.Map(location=[48, -102], zoom_start=3)
# I can add marker one by one on the map
for i in range(0,len(data)):
    folium.Marker([data.iloc[i]['latitude_deg'], data.iloc[i]['longitude_deg']], popup=data.iloc[i]['name']).add_to(m)
# output map
folium_static(m)

# # number of all airports
# st.write("Number of all airports: ")
# index = df.index
# number_of_rows = len(index)
# st.write(number_of_rows)

# #cal only
# cal = df[df["iso_region"] == "US-CA"]
# #number of cal airports
# st.write("Number of Cal airports: ")
# indexs = cal.index
# nums = len(indexs)
# st.write(nums)
# st.write(cal)

# #mexico only
# mxonly = df[df["iso_country"] == "MX"]
# #number of mexico airports
# st.write("Number of Mexico airports: ")
# inde = mxonly.index
# num = len(inde)
# st.write(num)
# st.write(mxonly.head(2000))

## example of maps
# m = folium.Map(location=[35, -100], zoom_start=2)
# # I can add marker one by one on the map
# for i in range(0,len(df.head(100))):
#     folium.Marker([df.iloc[i]['latitude_deg'], df.iloc[i]['longitude_deg']], popup=df.iloc[i]['name']).add_to(m)
# # output map
# folium_static(m)