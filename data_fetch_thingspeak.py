# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 16:43:50 2022

@author: Zied Tabelsi

"""

import urllib.request
import json
import time
import sqlite3
 

# open a connection to the SQLite database file healthup
conn = sqlite3.connect('healthup') 
# create a cursor k to execute some SQL commands
k = conn.cursor()

# Insert SQLite Statement: we need to insert 4 values into the table.
insert_statement = """
          INSERT INTO healthup (created_at, Heartrate, SpO2, Temperature)
               VALUES (?, ?, ?, ?)
        """          

# Thingspeak API Key    
READ_API_KEY='Y5ICXXPBFI2Z85CS'
# Thingspeak Channel ID   
CHANNEL_ID= '1623001'

# create 4 empty lists in order to append the data received from thingspeak:[created_at, Heartrate, SPo2, Temperature]
l_a = []
l_b = []
l_c = []
l_d = []
    
print('created_at       ','Heartrate    ','SpO2   ','Temperature   ')

# while: infinite Loop to retrieve data via API-Call "urllib.request.urlopen("https://api.thingspeak.com/channels/1623001/feeds/last.json?api_key=Y5ICXXPBFI2Z85CS"
while True:
    #request the last channel feed
    TS = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                       % (CHANNEL_ID,READ_API_KEY))
    
    # read the reponse (data)    
    response = TS.read()
    # data from thingspeak are in JSON Format so we load it in a variable of JSON format "data"
    data=json.loads(response)
    
    
    a = data['created_at']
    b = data['field1']
    c = data['field2']
    d = data['field3']
    print (a + "    " + b + "    " + c + "    " + d)
    #append every data point to the list values
    values = [a, b, c ,d]
    
    # execute the insertion of data into table "healthup"
    k.execute(insert_statement, values)
    # commit the execution
    conn.commit()
    # add the values to the Lists
    l_a.append(a)
    l_b.append(b)
    l_c.append(c)
    l_d.append(d)
    
    # as we are getting Data from Thingspeak every 22 sec, we have to wait 22 sec and then retrieve the next Data feed 
    time.sleep(22)

# close connection for the API-call
TS.close()
