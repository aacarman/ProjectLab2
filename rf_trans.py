from time import sleep              # creates a delay
from lib_nrf24 import NRF24         # radio library
import spidev                       # SPI library
import RPi.GPIO as GPIO             # GPIO pins

GPIO.setmode(GPIO.BCM)              # set GPIO mode as BCM mode (not physical)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1],     # where the data is going to be stored for writing/reading
         [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

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

while True:                                  # infinite loop
    buf = [1,2,3,4,5,6,7,8,9,0]              # create a list of data (must be shorter than 32, values must be 0 <= x <= 255)
    radio.write(buf)                         # write the data to the radio
    print ("sent"),                          # print what
    print (data)                             # we wrote
    sleep(1)                                 # delay for one second
