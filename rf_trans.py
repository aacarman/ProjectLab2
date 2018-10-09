from time import sleep
from lib_nrf24 import NRF24
import spidev
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1],
         [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())

radio.begin(0, 17)
radio.setPayloadSize(32)
radio.enableDynamicPayloads()
radio.setChannel(0x76)

radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])

while True:
    buf = [1,2,3,4,5,6,7,8,9,0]
    radio.write(buf)
    print ("sent"),
    print (data)
    sleep(1)
