##Data Retrieval Program
##
##Author: Aaron Carman
##Company: Texas Tech University
##
##Written for Project Lab 2
##Instructor: Derek Johnston
##Class Code-Section: ECE 3332-302
##
##Current Revision: 1.01
##
##Revision History:
##
##1.01: Implements correct filepath, parses data, outputs data on Python display
##
##1.00: Program Created, attempts to ping data from myRIO, receives error 404
##
##Program Description:
##
##This program takes data from the myRIO (filepath: "http://172.16.0.1:8001/FieldData/GetData") and
##loads the data as a Python dictionary. The advantage of dictionaries is that the data may be accessed
##by keys, making it more intuitive to the user.

import requests         ##used to ping data from myRIO
import json             ##used to load data as a python dict
from os import system   ##used to clear the output screen
from time import sleep  ##used to pause so we don't continuously output data

filepath = 'http://172.16.0.1:8001/FieldData/GetData'

while(1):       ##creates an infinite loop to continually retrieve and output data
    system('clear')                 ##clears screen
    url = requests.get(filepath)    ##get data from myRIO filepath
    data = json.loads(url.text)     ##turns JSON object into Python dict
    print(data['Ball']['Object Center'], sort_keys = True, indent = 4)
    ##         prints ball center              sorted      with an indentation to make it easier to see
    ball_x = data['Ball']['Object Center']['X']
    ball_y = data['Ball']['Object Center']['Y']
    sleep(1)    ##sleeps for 1 second
    
