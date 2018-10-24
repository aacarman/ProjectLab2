# Data Retrieval Program
#
# Author: Aaron Carman
# Company: Texas Tech University
# 
# Written for Project Lab 2
# Instructor: Derek Johnston
# Class Code-Section: ECE 3332-302
# 
# Current Revision: 2.00
# 
# Revision History:
#
# 2.00: Added RF transmission. Data is aligned in an array, and then transmit
#       through an NRF module.
# 
# 1.10: Parses all needed data. Performs operations to find key points.
#       Transforms data to Cartesian coordinates.
# 
# 1.02: Parses data and output on screen. Updates continuously.
# 
# 1.01: Implements correct filepath, parses data, outputs data on Python display
# 
# 1.00: Program Created, attempts to ping data from myRIO, receives error 404
# 
# Program Description:
# 
# This program takes data from the myRIO (filepath: "http://172.16.0.1:8001/FieldData/GetData") and
# loads the data as a Python dictionary. The advantage of dictionaries is that the data may be accessed
# by keys, making it more intuitive to the user. This data is then transformed into coordinate data. This
# coordinate data is then listed in an array. The array is transmit using the NRF module, and can be 
# received using a compatible NRF module.

import requests                              # used to ping data from myRIO
import json                                  # used to load data as a python dict
from os import system                        # used to clear the output screen
from time import sleep                       # used to pause so we don't continuously output data
from lib_nrf24 import NRF24                  # radio library
import spidev                                # SPI library
import RPi.GPIO as GPIO                      # GPIO pins

def transform(resolution, x2, x1, xin):
    m = float(float(resolution-1)/float(x2-x1))
    xT = float(m)*float(xin-x1)
    return xT
  
GPIO.setmode(GPIO.BCM)                       # set GPIO mode as BCM mode (not physical)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1],     # where the data is going to be stored for writing/reading
         [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]     # this is the address on the NRF board

radio = NRF24(GPIO, spidev.SpiDev())         # initialize radio object

radio.begin(0, 17)                           # begin the radio setup
radio.setPayloadSize(32)                     # set maximum payload size to 32 bytes (max)
radio.enableDynamicPayloads()                # enable dynamic payloads (shouldn't need it practically, but it makes for a good demo
radio.setChannel(0x76)                       # set the channel to transmit/receive on

radio.setDataRate(NRF24.BR_1MBPS)            # set the data transmission rate
radio.setPALevel(NRF24.PA_MAX)               # set the amplifier power to maximum
radio.setAutoAck(True)                       # set Auto Acknowledge (mostly for debugging)
radio.enableAckPayload()                     # enable the acknowledge payload

radio.openWritingPipe(pipes[0])              # open the corresponding pipe for writing

while(1):                                    # creates an infinite loop to continually retrieve and output data
    
    url = requests.get('http://172.16.0.1:8001/FieldData/GetData')    # get data from myRIO filepath
    data = json.loads(url.text)                                       # turns JSON object into Python dict
    
    ball_x = data['Ball']['Object Center']['X']                       # parses ball data
    ball_y = data['Ball']['Object Center']['Y']
    
    red_cir_x = data['Red Team Data']['Circle']['Object Center']['X']      # parses red team data
    red_cir_y = data['Red Team Data']['Circle']['Object Center']['Y']
    red_sqr_x = data['Red Team Data']['Square']['Object Center']['X']
    red_sqr_y = data['Red Team Data']['Square']['Object Center']['Y']
    red_tri_x = data['Red Team Data']['Triangle']['Object Center']['X']
    red_tri_y = data['Red Team Data']['Triangle']['Object Center']['Y']

    blue_cir_x = data['Blue Team Data']['Circle']['Object Center']['X']    # parses blue team data
    blue_cir_y = data['Blue Team Data']['Circle']['Object Center']['Y']
    blue_sqr_x = data['Blue Team Data']['Square']['Object Center']['X']
    blue_sqr_y = data['Blue Team Data']['Square']['Object Center']['Y']
    blue_tri_x = data['Blue Team Data']['Triangle']['Object Center']['X']
    blue_tri_y = data['Blue Team Data']['Triangle']['Object Center']['Y']

    t_corn_x1 = data['Corners'][0]['X']                                    # parses each corner's coordinates
    t_corn_y1 = data['Corners'][0]['Y']

    t_corn_x2 = data['Corners'][3]['X']
    t_corn_y2 = data['Corners'][3]['Y']

    t_ball_x = transform(256, t_corn_x2, t_corn_x1, ball_x)                # transforms all coordinates
    t_ball_y = transform(128, t_corn_y2, t_corn_y1, ball_y)

    t_red_cir_x = transform(256, t_corn_x2, t_corn_x1, red_cir_x)
    t_red_cir_y = transform(128, t_corn_y2, t_corn_y1, red_cir_y)
    t_red_sqr_x = transform(256, t_corn_x2, t_corn_x1, red_sqr_x)
    t_red_sqr_y = transform(128, t_corn_y2, t_corn_y1, red_sqr_y)
    t_red_tri_x = transform(256, t_corn_x2, t_corn_x1, red_tri_x)
    t_red_tri_y = transform(128, t_corn_y2, t_corn_y1, red_tri_y)

    t_blue_cir_x = transform(256, t_corn_x2, t_corn_x1, blue_cir_x)
    t_blue_cir_y = transform(128, t_corn_y2, t_corn_y1, blue_cir_y)
    t_blue_sqr_x = transform(256, t_corn_x2, t_corn_x1, blue_sqr_x)
    t_blue_sqr_y = transform(128, t_corn_y2, t_corn_y1, blue_sqr_y)
    t_blue_tri_x = transform(256, t_corn_x2, t_corn_x1, blue_tri_x)
    t_blue_tri_y = transform(128, t_corn_y2, t_corn_y1, blue_tri_y)

    tx_array = [t_ball_x, t_ball_y, t_red_cir_x, t_red_cir_y, \
                t_red_sqr_x, t_red_sqr_y, t_red_tri_x, t_red_tri_y, \
                t_blu_cir_x, t_blu_cir_y, t_blu_sqr_x, t_blu_sqr_y, \
                t_blu_tri_x, t_blu_tri_y]
    
    buf = tx_array                           # create a list of data (must be shorter than 32, values must be 0 <= x <= 255)
    radio.write(buf)                         # write the data to the radio
    print ("sent"),                          # print what we wrote
    print (buf)                             

    sleep(1)    # sleeps for 1 second
