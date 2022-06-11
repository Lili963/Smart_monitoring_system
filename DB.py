# -*- coding: utf-8 -*-
"""
Created on Sat Feb 5 10:40:54 2022

@author: Zied Tabelsi

"""

# database creation

import sqlite3
# create the database file healthup
conn = sqlite3.connect('healthup') 
c = conn.cursor()
# create a table that holds the health parameters
c.execute('''
          CREATE TABLE IF NOT EXISTS healthup
          (created_at TEXT UNIQUE ON CONFLICT FAIL,
           Heartrate INT, 
           SpO2 INT, 
           Temperature INT,
           PRIMARY KEY(created_at))
          ''')
# commit the current transaction                     
conn.commit()

