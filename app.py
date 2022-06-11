# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 22:12:26 2022

@author: Zied Trabelsi

"""

import streamlit as st 
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode

   
#configuration of the page
st.set_page_config(layout="wide")
#st.set_page_config(layout="centered")
# Set the Title of the App
st.title('Smart Health Care Monitoring System')
# Set markdown: Some Info about the App
st.markdown("""This app performs simple visualization of an IoT Data-retrieval Device - 
            Real-Time Patient Heartrate, Spo2 and Human Skin Temperature""")
# Set markdown: For patient records
st.header("Patient records")
st.markdown("""Patient ID: xxxxx""")
st.markdown("""Age: xxxxx""")
st.markdown("""Chronic diseases: xxxxx""")

st.header("Recent vital signs")
# Run the autorefresh about every 22000 milliseconds (22 seconds) 
st_autorefresh(interval=22000, key="fizzbuzzcounter")

    

# get_data () is a function to fetch/retrieve all the data saved in our Local Database "Healthup"
def get_data():    
    # open a connection "conn" to the SQLite database file "healthup" with specifying the Local repository PATH where we saved the Database file
    conn = sqlite3.connect(r'C:\Users\ziedt\zied_app_dev\zied_app_dev_v1\healthup') 
    # read_sql: read the select statement from the DB healthup. read all data within this table/DB 
    df = pd.read_sql('select * from healthup', conn)
    # drop_duplication(): we remove all duplicated Data
    df = df.drop_duplicates()
    # we round the temperature value of two integer after the comma
    df.Temperature = df.Temperature.round(2)
    # we round the SpO2 value of two integer after the comma
    df.SpO2 = df.SpO2.round(2)
    # Convert the "Created_at" values to seperate Date and Time 
    # 2022-03-26T19:16:33Z: df['Date']  =  "2022-03-26"
    df['Date'] = pd.to_datetime(df['created_at']).dt.date
    # 2022-03-26T19:16:33Z: df['Date']  =  "19:16:33"
    df['Time'] = pd.to_datetime(df['created_at']) 
    # .dt.time
    # as panda library returns the time in utc, we must add 2 hours to get back the timezone of Berlin 
    df['delta']=2
    df['delta'] = pd.to_timedelta(df['delta'], unit='h')
    df['Time'] += df['delta'] 
    df['Time'] = df['Time'].dt.time
    # when we call this function it returns a Dataframe of 6 Columns; created_at, Date, Time, 'Heartrate', 'SpO2', 'Skin Temperature' 
    return(df)

#call function get_data() to fetch data from healthup DB and assign it to the dataframe called df_healthup
df_healthup = get_data()

# get_data_aggrid(): function in order to prepare the data to display it in Table - Last charts in the App.
def get_data_aggrid(df_healthup):
    # remove first column created_at as we have converted date and time for Table visualization
    # the dataframe assigned to new variable data
    data = df_healthup.iloc[:,1:]
    # new column order
    neworder = ['Date', 'Time', 'Heartrate', 'SpO2', 'Temperature']
    #assign the new columns order to the dataframe data
    data=data.reindex(columns=neworder)
    # change column names for better understanding
    data.columns = ['Date', 'Time', 'Heartrate (BPM)', 'SpO2 (%)', 'Skin Temperature (°C)']
    #return dataframe data after the changes 
    return(data)


# Display the Recent vital signs in big bold font in form of 3 columns
col1, col2, col3 = st.columns(3)

col1.metric("Heartrate", df_healthup.iloc[-1,2], "Beats per minute BPM")
col2.metric("SpO2", df_healthup.iloc[-1,3], "percent (%)")
col3.metric("Skin Temperature", df_healthup.iloc[-1,4], "Degrees Celsius (°C)")

# Subplots Plotly's Python graphing library: 
# rows = 3 => we have three Stacked Subplots with shared X-Axes 
fig = make_subplots(rows=3,cols=1,shared_xaxes=True,vertical_spacing=0.1, subplot_titles=("Heartrate (BPM)", "SpO2 (%)", "Skin Temperature (°C)"))
# grab only the last 50 data points for to get a smaller scale in charts
df_healthup_sc = df_healthup.tail(50)

#First SubPlot
fig.add_trace(
    go.Scatter(
        x=df_healthup_sc["Time"], 
        y=df_healthup_sc["Heartrate"],mode='lines+markers',
                    name='Heartrate'),
        row=1, col=1
    )

#Second SubPlot
fig.add_trace(
    go.Scatter(
    x=df_healthup_sc["Time"], 
    y=df_healthup_sc["SpO2"],mode='lines+markers',
                name='SpO2'), 
        row=2, col=1
    )

#Third SubPlot
fig.add_trace(
    go.Scatter(
    x=df_healthup_sc["Time"], 
    y=df_healthup_sc["Temperature"],mode='lines+markers',
                name='Skin Temperature'),
        row=3, col=1
    )

fig.update_layout(height=750, width=1000,showlegend=False, margin=dict(
        l=0,
        r=50,
        b=100,
        t=100,
        pad=4
    ))

st.header("Vital signs history")
st.plotly_chart(fig)

# displaying dataframe using the streamlit-aggrid component
# call function get_data_aggrid()to get the dataframe with changes needed to be visualized
data = get_data_aggrid(df_healthup)
#  add options to the AgGrid Table
gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_side_bar() #Add a sidebar
gridOptions = gb.build()

# Visualize Aggrid Table
AgGrid(
    data,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode= GridUpdateMode.MODEL_CHANGED, 
    fit_columns_on_grid_load=False,
    theme='blue', #Add theme color to the table
    enable_enterprise_modules=True,
    height=400, 
    width=None,
    reload_data=True
    )



    